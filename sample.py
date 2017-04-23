import webbrowser
import sys
import os


#---------------------------------HTMLReport------------------------------------
def HTMLReport():
	try:
		reportName = "heartbeat"
		clientID = "100100"
		avgHeartBeat = 80

		# Create the HTML file for output
		htmlReportPath = os.path.dirname(os.path.realpath(__file__))
		htmlReportPath = os.path.join(htmlReportPath,"report.html")
		print htmlReportPath
		htmlReport = open(htmlReportPath,"w")

		# write html document
		global html
		html = """
		<!DOCTYPE html>
		<html>
		<head>
			<title>Sample Report</title>
			<style>
			.wrapper  {
				width: 100%;
				height: 100%;
				background-color: #FFF;
				cursor: default;
			}

			.report {
				font-family: Arial;
				font-size: 10px;
				border-width: 1px;
				border-spacing: 1px;
				border-style: outset;
				border-color: gray;
				border-collapse: separate;
				padding: 0px;
				background: #FFF;
			}

			.report tr:hover {
				background-color: #DBDBFF;
			}

			.heading {
				font-family: Arial;
				font-size: 18px;
				font-weight: 900;
				padding: 50px;
				color: #3399FF;
				margin-left: 20px;
			}

			.report th {
				background: #59ACFF;
				color: white;
			}

			.report td,th{
				border-width: 0.5px;
				border-style: inset;
				border-color: white;
				border-collapse: collapse;
				padding: 10px;
			}

			.logo {
				width: 130px;
				height: 100px;
				float: left;
				padding: 30px;
			}

			.caption {
				font-family: Arial;
				font-size: 14px;
				font-weight: 900;
				padding: 10px;
			}
			</style>
		</head>

		<body class="main">
		<header>
			<h1 class="heading">Report: """ + reportName + """ Client ID: """ + clientID + """</h1>
			<h3 class="caption"> Average """ + reportName + """: """ + str(avgHeartBeat) + """</h3>
		</header>
		<div class="wrapper">
			<p> Hello </p>
		<br/>
		"""

		htmlReport.write(html)

		# write all closing tags
		htmlReport.write('</div>')
		htmlReport.write('</body>')
		htmlReport.write('</html>')

		# print results to shell
		print "Created html report"
		htmlReport.close()

		webbrowser.get().open(htmlReportPath)

		return 0

	except:
		comment = ('EXCEPTION: ' + str(sys.exc_info()[1]))
		print comment
		return 0

if __name__ == '__main__':
    HTMLReport()