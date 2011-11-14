import SentenceTree as st
import ResultPrinter as rp
import lemma_pos as lp

#x = st.SentenceTree()
#printer = rp.ResultPrinter()
#printer.write(2, "YES")


#one = lp.OneB()
# TRUE = lemma, FALSE = lemma && POS
#one.printResults(False)

data = st.SentenceTree(False)
print data.getDf("father")
