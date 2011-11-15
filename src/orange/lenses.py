import orange
data = orange.ExampleTable("lenses")
print "Attributes:",
for i in data.domain.attributes:
    print i.name,
print
print "Class:", data.domain.classVar.name

print "First 5 data items:"
for i in range(5):
   print data[i]
   
orange.saveTabDelimited ("data.tab", data)
