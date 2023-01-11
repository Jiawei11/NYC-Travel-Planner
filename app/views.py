from flask import Flask, jsonify
import json
import flask
import datetime
import psycopg2

conn = psycopg2.connect(
    host="localhost", 
    database="postgres",
    user="postgres",
    password="123")

# create a cursor
cur = conn.cursor()

app = flask.Flask(__name__)

@app.route("/")
def index():
    
    return flask.render_template("index.html")

@app.route("/index2")
def index2():
    return flask.render_template("index2.html")

@app.route("/index3")
def index3():
    return flask.render_template("index3.html")

@app.route("/index4")
def index4():
    return flask.render_template("index4.html")

@app.route("/autoComplete")
def autoComplete():
    # elastic search for zipcodes, give searching result when users typing
    word = flask.request.args.get("word")
    if not word:
        arr = []
    else:    
        query1 = """
                select distinct cast(zipcodes as VARCHAR) from geometry g where cast(zipcodes as VARCHAR) like '{}%'
            """
        # Execute the statement and get the results
        print(query1.format([word]))
        cur.execute(query1.format(word))
        arr = cur.fetchall()
        # Add the information to the dataframe
    return jsonify(arr)

@app.route("/queryRoom")
def queryRoom():
    # elastic search for zipcodes, give searching result when users typing
    zipcode = flask.request.args.get("word")
    querySql = '''
        select g.id,l.name,l.description,u.picture_url,p.price  from listing l left join geometry g on l.listing_id = g.id 
        left join url u on u.id = l.listing_id
        left join price p on p.id = l.listing_id 
        where g.zipcodes = {}
    '''
    # querying the total number of rooms as count
    # querying the average price of returned rooms
    countSql = '''
        select count(1),CAST(avg(p.price) as DECIMAL(18,2))  from listing l left join geometry g on l.listing_id = g.id 
        left join url u on u.id = l.listing_id
        left join price p on p.id = l.listing_id 
        where g.zipcodes = {}    
    '''
    cur.execute(querySql.format(zipcode))
    rows = cur.fetchall()
    cur.execute(countSql.format(zipcode))
    count = cur.fetchone()
    return flask.render_template("products.html",
                                    rooms = rows,zipcode = zipcode,count = count)

@app.route("/queryRoomDetail", methods=["GET"])
def queryRoomDetail():
    """
    get room info using id
    """
    id = flask.request.args.get("item")
    querySql = '''
        select l."name" ,l.description ,h.host_name ,u.picture_url,p2.price,s.star,  
        p.room_type ,p.bathrooms ,p.bedrooms ,p.amenities,
        h.host_name ,h.host_since ,h.host_location,h.host_neighbourhood,
        r.first_review ,r.last_review ,r.review_scores_rating,r.review_scores_accuracy,r.review_scores_cleanliness ,
        r.review_scores_checkin ,r.review_scores_communication ,r.review_scores_location ,r.review_scores_value,
        h.host_response_time ,h.host_response_rate ,h.host_response_rate,
        p.beds ,p.accommodates 
        from listing l
        left join "host" h  on l.listing_id  = h.host_id 
        left join property p on p.property_id = l.listing_id
        left join price p2 on p2.id =  l.listing_id
        left join stars s on s.id = l.listing_id 
        left join url u on u.id = l.listing_id
        left join review r on r.review_id = l.listing_id 
        where l.listing_id = {}
    '''
    """
    get crime report nearby of this room
    """
    crimeSql = '''
        select crime_type, count(1) from crime_geometry cg 
        left join crime_type ct on cg.case_num = ct.case_num  
        left join geometry g on cg.zipcodes = g.zipcodes 
        where g.id= {} group by crime_type order by count(1) desc

    '''

    cur.execute(querySql.format(id))
    room = cur.fetchone()
    cur.execute(crimeSql.format(id))
    criminal = cur.fetchall()
    return flask.render_template("product.html",item=room,criminal=criminal)

@app.route("/queryRestaurant")
def queryRestaurant():
    # elastic search for zipcodes, give searching result when users typing
    zipcode = flask.request.args.get("word")
    querySql = '''
		SELECT name,neighbourhood,building,street,phone
		FROM restaurants
		WHERE zipcode = {}
    '''
    countSql = '''
		SELECT count(1)
		FROM restaurants
		WHERE zipcode = {}  
    '''
    cur.execute(querySql.format(zipcode))
    rows = cur.fetchall()
    cur.execute(countSql.format(zipcode))
    count = cur.fetchone()
    return flask.render_template("restaurants.html",
                                    rows = rows,zipcode = zipcode,count = count)

@app.route("/queryMichelinRestaurant")
def queryMichelinRestaurant():
    # elastic search for zipcodes, give searching result when users typing
    zipcode = flask.request.args.get("word")
    querySql = '''
        SELECT name, year AS award_year, cuisine, price, url, star
        FROM Michelin_restaurants mr
        JOIN stars s ON mr.id = s.id
        where mr.zipcode = {}
    '''
    countSql = '''
		SELECT count(1)
		FROM Michelin_restaurants
		WHERE zipcode = {}  
    '''
    cur.execute(querySql.format(zipcode))
    rows = cur.fetchall()
    cur.execute(countSql.format(zipcode))
    count = cur.fetchone()
    return flask.render_template("michelin.html",
                                    rows = rows,zipcode = zipcode,count = count)

@app.route("/queryCriminal")
def queryCriminal():
    # elastic search for zipcodes, give searching result when users typing
    zipcode = flask.request.args.get("word")
    querySql = '''
        SELECT case_num, crime_type
        FROM crime_type
        JOIN crime_geometry using(case_num)
        WHERE zipcodes = {}
    '''
    countSql = '''
        SELECT count(1)
        FROM crime_type
        JOIN crime_geometry using(case_num)
        WHERE zipcodes = {}  
    '''
    cur.execute(querySql.format(zipcode))
    rows = cur.fetchall()
    cur.execute(countSql.format(zipcode))
    count = cur.fetchone()
    return flask.render_template("criminal.html",
                                    rows = rows,zipcode = zipcode,count = count)
app.run()