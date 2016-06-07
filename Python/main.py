#!/usr/bin/python
# coding: utf-8

"""
point2map_v03 ist fuer die console und Rechner PC-31 bestimmt!

TODO: Hinzufügen von neuen Layern (PDF Seiten)
1. Layername in views liste aufnehmen
2. Zoommaßstab für neuen "View" in views-Liste aufnehmen
3. Neuen Legendeneintrag ab Zeile 255 einfügen
4. neuen Legendeneintrag wieder in den "unsichtbaren" Bereich verschieben (ab Zeile 250)


"""

import arcpy,os,time,codecs,sys
from ConfigParser import SafeConfigParser

""" PATHS """
scriptPath = "C:/GIS/Python_Tools/point2map_v03/Python"
pdfRootPath = "N:/Start_Script/"
projectPATHS = {}
projectPATHS["DEFAULT"] = "N:/Unterlagen/Geologische Karten/Projekte_SCRIPT/Projekte DEFAULT.shp"
projectPATHS["GT"] = "N:/Unterlagen/Geologische Karten/Projekte_GT/Projekte GT.shp"
projectPATHS["ALT"] = "N:/Unterlagen/Geologische Karten/Projekte_ALT/Projekte ALT.shp"
projectPATHS["HYD"] = "N:/Unterlagen/Geologische Karten/Projekte_HYD/Projekte HYD.shp"
projectPATHS["EWS"] = "N:/Unterlagen/Geologische Karten/Projekte_EWS/Projekte EWS.shp"

pdfRootPath = os.path.normpath(pdfRootPath)


""" Data input via config.file """
print "Starte point2db-Skript\t{0}\t{1}".format(time.strftime("%H:%M:%S"),(time.strftime("%d/%m/%Y")))
parser = SafeConfigParser()
with codecs.open('N:/Start_Script/new_point.txt', 'r', encoding='utf-8-sig') as f:
    """    first = f.read(1)
    if first != '\ufeff':
        # not a BOM, rewind
        f.seek(0)
    """
    parser.readfp(f)

""" Id Az Bez Geologie """

print "Read in following arguments:\n"
print parser.get('Pflichtfelder','x')
print parser.get('Pflichtfelder','y')
print parser.get('Pflichtfelder','az')
print parser.get('Pflichtfelder','BV')

x =  float(parser.get('Pflichtfelder','x'))
y =  float(parser.get('Pflichtfelder','y'))
az =  parser.get('Pflichtfelder','az')
try:
    az = unicode(az)
except:
    print "Fehler beim einlesen von az"
BV = parser.get('Pflichtfelder','BV')
try:
    BV = u''+BV
except:
    print "Fehler beim einlesen von BV"
geologie =  parser.get('Optional','geologie')
try:
    geologie = unicode(geologie)
except:
    print "Geologie nicht gefunden:"
    geologie = None

""" Extract Data for Project point """
try:
    category = parser.get('Pflichtfelder','Kategorie')
    try:
        category = u''+category
    except:
        print "Could not resolve category."
except:
    print "No arguments found. A Project point will not be added!"


''' CHECK INPUT AND GET SPECIFIC SHAPEFILE'''
try:
    projectDEFAULT = projectPATHS[category]
except:
    print "Could not find shapefile. Inserting in default file located under: N:/Unterlagen/Geologische Karten/Projekte_SCRIPT/Projekte_SCRIPT.shp"
    projectDEFAULT = projectDEFAULT

''' CHECK IF AZ EXISTS IN DB '''
feature = projectDEFAULT
field = 'Az'
cursor = arcpy.SearchCursor(feature)
for row in cursor:
    if (az ==(row.getValue(field))):
        print "Db Entry already exists... stopping execution."
        sys.exit()
        break

''' POCEEDING WITH ADDING DATA TO PROJECT POINT '''
try:
    """ Id Az Bez Geologie """
    rowInserter = arcpy.InsertCursor(projectDEFAULT)
    rowUpdater = arcpy.UpdateCursor(projectDEFAULT)
    pointGeometry = arcpy.Point(x,y)
    newPoint = rowInserter.newRow()

    newPoint.Shape = pointGeometry
    # add az to point
    if not az == None:
        newPoint.Az = az
    # add BV data to bez (Bezeichnung)
    if not BV == None:
        newPoint.Bez = BV

    if not geologie == None:
        newPoint.Geologie = geologie

    rowInserter.insertRow(newPoint)

    del rowInserter
except:
    print("Could not add project point. Exiting now...")
