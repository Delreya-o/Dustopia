# Projet CMI
## Contexte
Dans le cadre d'un projet de groupe en première année de licence informatique, nous avons créé un mini jeu vidéo inspiré des jeux de plateforme.
Le langage étant libre, nous avons décidé de coder le jeu en Python, en utilisant la librairie PyGame.

## Le jeu
### L'histoire

Cette histoire se déroule dans une dystopie. Une entreprise dirigée par les humains, dont le dirigeant est un certain Bob, se propage de plus en plus dans la galaxie. Cette entreprise ravage des civilisations entières et exploite la puissance des étoiles dans le seul but de préserver sa propre existence.

Kaku, un susuwatari comme les autres, décide d’empêcher cette catastrophe morale. En passant par une planète dénommée Terre, cette petite boule de suie découvre que les humains emprisonnent et exterminent les susuwataris un par un pour récupérer leur Dust.

Ainsi, le but de notre petit susuwatari est de libérer ses amis en récupérant un maximum d’étoiles, puis de rentrer sur sa planète d’origine. Mais il doit faire attention, car les humains ont créé des gardiens pour empêcher les susuwataris de s’enfuir.

### Principe / But

Le joueur contrôle Kaku. Il peut se déplacer à gauche, à droite et sauter en utilisant les flèches directionnelles.

Un niveau est composé de plusieurs blocs sur lesquels Kaku doit marcher, sauter ou contourner des obstacles pour atteindre la fin du niveau, où il trouvera un autre susuwatari. Mais s’il tombe dans un trou, il meurt, et le joueur doit recommencer le niveau.

Sur le chemin, il peut rencontrer des poubelles qui génèrent trois types de monstres : des balais, des sprays et des aspirateurs, que le joueur devra esquiver (en sautant par-dessus, par exemple). Si, par malheur, Kaku ne parvient pas à les éviter, il perd une vie et meurt s’il a perdu ses trois vies.

La barre de vie est réinitialisée à chaque début de niveau.
