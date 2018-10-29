import point

asd = point.point(5, 8)
qwe = point.point(1, 2)
dic = {'x': 1, 'y': 1}
eqasd = point.point(5, 8)
diceqasd = {'x': 5, 'y': 8}
neasd = point.point(4, 8)
oneone = {'x': 1, 'y': 1}
updic = {u'x': 5, u'y': 8}
dirs = ['up', 'down', 'right', 'left']

print("Substraction:")
print("%s - %s = %s" % (str(asd), str(qwe), str(asd - qwe)))
print("%s - %s = %s" % (str(asd), str(dic), str(asd - dic)))
print("%s - %s = %s" % (str(asd), str(updic), str(asd - updic)))
                      
print("Addition:")    
print("%s + %s = %s" % (str(asd), str(qwe), str(asd + qwe)))
print("%s + %s = %s" % (str(asd), str(dic), str(asd + dic)))
print("%s + %s = %s" % (str(asd), str(updic), str(asd + updic)))

print("Equality:")
print("%s == %s = %s" % (str(asd), str(qwe), str(asd == qwe)))
print("%s == %s = %s" % (str(asd), str(dic), str(asd == dic)))
print("%s == %s = %s" % (str(asd), str(diceqasd), str(asd == diceqasd)))
print("%s == %s = %s" % (str(asd), str(updic), str(asd == updic)))


print("NEquality:")
print("%s != %s = %s" % (str(asd), str(qwe), str(asd != qwe)))
print("%s != %s = %s" % (str(asd), str(dic), str(asd != dic)))
print("%s != %s = %s" % (str(asd), str(diceqasd), str(asd != diceqasd)))
print("%s != %s = %s" % (str(asd), str(updic), str(asd != updic)))

sdic = {u'x': 1, u'y': 1}
points = [ point.point(1,1), point.point(1,2) ]

print("In list")
if oneone in points:
    print("%s in list" % str(oneone))
else:
    print("%s not in list" % str(oneone))
    
if qwe in points:
    print("%s in list" % str(qwe))
else:
    print("%s not in list" % str(qwe))
    
if sdic in points:
    print("%s in list" % str(sdic))
else:
    print("%s not in list" % str(sdic))

print("topoint(%s) = %s" % (str(oneone), str(point.topoint(oneone))))

for dir in dirs:
    print("topoint(%s) = %s" % (dir, str(point.topoint(dir))))

negpoint = point.point(-5,-5)
print("dist:")
print("%s.dist() = %s" % (str(asd), str(asd.dist())))
print("%s.dist() = %s" % (str(neasd), str(neasd.dist())))
print("%s.dist() = %s" % (str(negpoint), str(negpoint.dist())))

print("Rotate:")
for dir in dirs:
    print("%s rotated CCW: %s" % (dir, point.topoint(dir).rotateCCW().todir()))
    print("%s rotated CW: %s" % (dir, point.topoint(dir).rotateCW().todir()))
