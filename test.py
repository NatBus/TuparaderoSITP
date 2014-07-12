import web
render = web.template.render('templates/')

urls   = (
	'/', 'index'
	)
app = web.application(urls, globals())

class index:
	def GET(self):
		return "Hello, world"

app.run()