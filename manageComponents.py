import components.component as cpt
import gilgamesh as gilga

cpt.initComponentDB()
ishtar=cpt.Testbed('IShTAR')
diags=cpt.Diagnostics('Diagnostics')
probe1=cpt.LangmuirProbe('Langmuir1','cylNC',0.0002,0.03,'Lang_U','Lang_I')
diags.add_child(probe1)
ishtar.add_child(diags)
cpt.save('v1',ishtar)
liste=gilga.listShots(criterion='index>1000&index<=1300')
listshots=liste.index.values
cpt.attachShot('v1',listshots)
cpt.componentShot()
