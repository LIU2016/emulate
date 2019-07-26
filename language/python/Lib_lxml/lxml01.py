from lxml import etree

tree=etree.parse('product.xml')
#print(str(etree.tostring(tree,encoding='utf-8'),'utf-8'))

root = tree.getroot()
print(root.tag)

childrens = root.getchildren()
for ch in childrens:
    print(ch.get('id'))
    print(ch[0].text)
    print(ch[1].text)
    print(ch[2].text)

print("------------------------")
 #装载
root = etree.fromstring('''
    
 <products>
    <product id="003">
        <name>twsm</name>
        <ids>8</ids>
        <describe>soso</describe>
    </product>
    <product id="005">
        <name>twsm2</name>
        <ids>8</ids>
        <describe>soso2</describe>
    </product>
</products>
 ''')

childrens = root.getchildren()
for ch in childrens:
    print(ch.get('id'))
    print(ch[0].text)
    print(ch[1].text)
    print(ch[2].text)