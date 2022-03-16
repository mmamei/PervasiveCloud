import matplotlib.pyplot as plt

y = [4,5,6]
names = ['a','b','c']
plt.xticks([0,1,2], names)
plt.bar(range(len(y)),y)
plt.savefig('foo.png')
plt.show()
