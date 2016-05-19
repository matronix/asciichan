xml = """<HostipLookupResultSet xmlns:gml="http://www.opengis.net/gml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.0.1" xsi:noNamespaceSchemaLocation="http://www.hostip.info/api/hostip-1.0.1.xsd">
           <gml:description>This is the Hostip Lookup Service</gml:description>
           <gml:name>hostip</gml:name>
           <gml:boundedBy>
             <gml:Null>inapplicable</gml:Null>
           </gml:boundedBy>
           <gml:featureMember>
             <Hostip>
               <ip>12.215.42.19</ip>
               <gml:name>Aurora, TX</gml:name>
               <countryName>UNITED STATES</countryName>
               <countryAbbrev>US</countryAbbrev>
               <!-- Co-ordinates are available as lng,lat -->
               <ipLocation>
                 <gml:pointProperty>
                   <gml:Point srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">
                     <!--gml:coordinates>-97.5159,33.0582</gml:coordinates-->
                     <!--gml:coordinates></gml:coordinates-->
                   </gml:Point>
                 </gml:pointProperty>
               </ipLocation>
             </Hostip>
           </gml:featureMember>
        </HostipLookupResultSet>"""

# QUIZ - implement the get_coords(xml) function that takes in an xml string 
# and returns a tuple of (lat, lon) if there are coordinates in the xml.
# Remember that you should use minidom to do this.
# Also, notice that the coordinates in the xml string are in the format:
# (lon,lat), so you will have to switch them around.

from xml.dom import minidom

def get_coords(xml):
    TAG_NAME='gml:coordinates'
    #get the document object from the xml string so you can
    #parse it using Document methods such as getElementByTagName()
    doc1 = minidom.parseString(xml)

    #getElementByTagName() will return a NodeList and the item we want is index 0
    e = doc1.getElementsByTagName(TAG_NAME)
    i = e.item(0)

    try:
        if e and i.childNodes[0].nodeValue:
            coords = str(i.childNodes.item(0).data)
            coordsList = coords.split(',')
            return (coordsList[1],coordsList[0])
        else:
            return None
    except IndexError:
        return None
    

    
print get_coords(xml)
    

    

    
    
