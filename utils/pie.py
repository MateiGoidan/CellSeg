import matplotlib.pyplot as plt

# Numele claselor și numărul de exemple per clasă
class_labels = [
   "Rod", "RBC/WBC", "Yeast", "Misc",
  "EPC"
]

class_counts = [
  1697, 1056, 41, 550,
  218
]

# Culori personalizate (opțional)
colors = plt.cm.Paired.colors

# Creare diagramă circulară
plt.figure(figsize=(5, 5))
plt.pie(class_counts, labels=class_labels, autopct='%1.1f%%', startangle=140, colors=colors)
plt.title("Class Distribution in the Dataset")
plt.axis('equal')  # Păstrează aspectul circular

plt.show()

