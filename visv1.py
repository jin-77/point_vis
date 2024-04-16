import numpy as np
import pyviz3d.visualizer as viz
import plyfile
import os
from tqdm import tqdm 

def read_ply_data(filename):
    ply_data = plyfile.PlyData.read(filename)
    vertices = ply_data['vertex']
    x = np.array(vertices['x'])
    y = np.array(vertices['y'])
    z = np.array(vertices['z'])
    red = np.array(vertices['red'])
    green = np.array(vertices['green'])
    blue = np.array(vertices['blue'])
    intensity = np.array(vertices['intensity'])  # 仮の属性名
    label = np.array(vertices['label'])  # 仮の属性名
    
    return x, y, z, red, green, blue, intensity, label

def generate_color_map(unique_labels):
    np.random.seed(42)  # For reproducible colors; remove if random colors are desired each run
    color_map = {label: np.random.randint(0, 256, size=3) for label in unique_labels}
    return color_map

def main():
    prefix = './'
    name = 'sample_out'
    htmlname = 'ex'

    C_dis = 1.5  #0.15
    C_high = 1.5  #0.5


    x, y, z, red, green, blue, intensity, label = read_ply_data(os.path.join(prefix, name + ".ply"))
    point_positions = np.stack([x, y, z], axis=-1)
    centroid = np.mean(point_positions, axis=0)
    point_positions -= centroid

    camera_distance = np.max([np.abs(np.max(x)), np.abs(np.max(y))]) * C_dis # 0.15 最大のxまたはyの広がりの0.15倍
    camera_height = np.max(z) * C_high # カメラの高さを調整 
    camera_position = np.array([camera_distance, camera_distance, camera_height])

    look_at_position = np.array([0.0, 0.0, 0.0])

    v = viz.Visualizer(position=camera_position, look_at=look_at_position, up=np.array([0.0, 0.0, 1.0]), focal_length=28.0)

    unique_labels = np.unique(label)
    color_map = generate_color_map(unique_labels)

    #label_names = {0: 'other', 2: 'laneline', 10: 'sign', 15: 'light'}

    #label_names = {1: 'road', 2: 'laneline', 3: 'tree', 6: 'pole', 7:'building', 8:'other'}

    label_names = {1: 'road', 2: 'laneline', 3: 'tree', 10:'building'}



    # ラベルごとに点群を追加
    for lbl in tqdm(unique_labels, desc="Processing labels"):  
        lbl_indices = label == lbl
        lbl_positions = point_positions[lbl_indices]
        lbl_colors = np.tile(color_map[lbl], (lbl_positions.shape[0], 1)) 
        lbl_name = label_names.get(lbl, f'label_{lbl}')
        v.add_points(lbl_name, lbl_positions, lbl_colors, point_size=100, visible=True)

    # セマンティックカラーで全点群を追加
    semantic_colors = np.array([color_map[lbl] for lbl in label], dtype=np.float32)
    v.add_points('Semantic Color', point_positions, semantic_colors, point_size=100, visible=True)

    # オリジナルのRGBカラーで全点群を追加
    original_colors = np.stack([red, green, blue], axis=-1) / 255.0
    v.add_points('Original RGB Color', point_positions, original_colors, point_size=100, visible=True)

    v.save(f'{htmlname}.html')

if __name__ == '__main__':
    main()
