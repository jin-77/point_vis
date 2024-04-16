# txt convert ply
>python plyv1.py --input example.txt --output example_shifted --shift_to_origin

# modify visv1.py
>name, htmlname, label_names 

>def main():
	name = 'sample_out' 
	htmlname = 'ex' 
	label_names = {n1: 'name', n2: 'name', n3: 'name', n4:'name'} 

# make html for point visualization
>python visv1.py

# Examples
## ①ex.html
https://jin-77.github.io/example/

## ②Segmentation results for sign:traffic light:laneline:roadmarks 
https://jin-77.github.io/Segmentation_4class/

## ③Segmentation results for laneline:road:tree:buildings:pole:other
https://jin-77.github.io/Segmentation_6class/

## Refarence
このプロジェクトでは、Francis Engelmannによって開発されたPyViz3Dのコードが使用されています。詳細は以下のリンクを参照してください：
https://github.com/francisengelmann/PyViz3D

PyViz3DはMITライセンスのもとで公開されており、本プロジェクトでもそのライセンス条件に従います。ライセンスの全文は以下から確認できます：
https://github.com/francisengelmann/PyViz3D/blob/main/LICENSE
