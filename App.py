#importing the required library for DB connection
import psycopg2

def popularArticles():
	# printing the requirement statement
	print("What are the most popular three articles of all time?")
	# setting connection to database and specifiying the db name
	db = psycopg2.connect("dbname=news")
	c = db.cursor()

	c.execute("SELECT articles.title , count(*)	FROM articles, log WHERE log.path = CONCAT('/article/',articles.slug) GROUP BY articles.title,articles.slug ORDER BY 2 DESC	LIMIT (3);")
	result = c.fetchall()
	
	# loop the result three times as we know the number of required records
	for i in range(0,3,1):
		print (result[i][0] + " - " + str(result[i][1]) + " Views")
	db.close()

def popularAuthors():
	# printing the requirement statement
	print("Who are the most popular article authors of all time?")
	
	# setting connection to database and specifiying the db name
	db = psycopg2.connect("dbname=news")
	c = db.cursor()

	# assigning and execute sql statement via cursor
	c.execute("SELECT articles.author , count(articles.author) , authors.name FROM articles,authors,log	WHERE articles.author=authors.id AND log.path=CONCAT('/article/' , articles.slug) GROUP BY articles.author , authors.name ORDER BY 2 DESC;")
	result = c.fetchall()

	for i in range(0,len(result),1):
		print (result[i][2] + " - " + str(result[i][1]) + " Views")
	db.close()

def viewCreations():
	# setting connection to database and specifiying the db name
	db = psycopg2.connect("dbname=news")
	c = db.cursor()

	# assigning and execute sql statement via cursor to create the needed views
	c.execute("CREATE OR REPLACE VIEW error_status_view	AS SELECT date(time),count(*) as error_views FROM log WHERE status = '404 NOT FOUND' GROUP BY 1;")
	c.execute("CREATE OR REPLACE VIEW all_status_view AS SELECT date(time),count(*) as all_views FROM log GROUP BY 1;")
	c.execute("CREATE OR REPLACE VIEW percentage_view AS SELECT all_status_view.date, (1.0*error_status_view.error_views / all_status_view.all_views)*100.0 AS percentage_value FROM error_status_view,all_status_view WHERE all_status_view.date = error_status_view.date GROUP BY 1,2")
	# saving changes to db
	db.commit()
	db.close()

def errorPercentage():
	# printing the requirement statement
	print("On which days did more than 1% of requests lead to errors?")
	
	# setting connection to database and specifiying the db name
	db = psycopg2.connect("dbname=news")
	c = db.cursor()

	# assigning and execute sql statement via cursor
	c.execute("SELECT date, percentage_value FROM percentage_view where percentage_value > 1")

	result = c.fetchall()
	for i in range(0,len(result),1):
		print(str(result[i][0]) + "   -   " + str('{0:.2f}'.format(result[i][1])) + " % Errors")
		#print(str(result[0][1]))
	
	db.close()
	return result

if __name__ == '__main__':
	popularArticles()
	popularAuthors()
	viewCreations()
	errorPercentage()
	print ("App finish running !")
