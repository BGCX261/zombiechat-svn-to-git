from xml.sax import saxutils

class XmlWriter(object):
  def __init__(self, response):
    self.out = response.out
    response.headers['Content-Type'] = 'text/xml'
    response.out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        
  def Start(self, tag):
    self.out.write("<%s>" % tag)

  def End(self, tag):
    self.out.write("</%s>" % tag)
    
  def Content(self, tag, content):
    self.Start(tag)
    self.out.write(saxutils.escape(content).encode('UTF-8'))
    self.End(tag)