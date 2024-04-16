import numpy as np
import plyfile
import argparse
import os
from tqdm import tqdm  

def save_ply(filename, x, y, z, red, green, blue, intensity, label):
    with open(filename + '.ply', 'w') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write("element vertex {}\n".format(len(x)))
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("property uchar intensity\n")
        f.write("property short label\n")
        f.write("end_header\n")
        
        
        for i in tqdm(range(len(x)), desc="Saving PLY"):
            f.write("{} {} {} {} {} {} {} {}\n".format(x[i], y[i], z[i], red[i], green[i], blue[i], intensity[i], label[i]))

def read_ply_and_adjust_data_types(filename):
    ply_data = plyfile.PlyData.read(filename)
    vertices = ply_data['vertex']
    
    x = np.array(vertices['x'], dtype=np.float32)
    y = np.array(vertices['y'], dtype=np.float32)
    z = np.array(vertices['z'], dtype=np.float32)
    red = np.array(vertices['red'], dtype=np.uint8)
    green = np.array(vertices['green'], dtype=np.uint8)
    blue = np.array(vertices['blue'], dtype=np.uint8)
    intensity = np.array(vertices['scalar_Intensity'], dtype=np.float32)
    label = np.array(vertices['scalar_label'], dtype=np.float32)
    
    return adjust_data_types(x, y, z, red, green, blue, intensity, label)

def read_txt_and_adjust_data_types(filename):
    data = np.loadtxt(filename, skiprows=2)
    x, y, z = data[:, :3].T
    red, green, blue, intensity, label = data[:, 3:8].T
    
    return adjust_data_types(x, y, z, red, green, blue, intensity, label)

def adjust_data_types(x, y, z, red, green, blue, intensity, label):
    # RGB 値を uint8 型に変換
    red = red.round().astype(np.uint8)
    green = green.round().astype(np.uint8)
    blue = blue.round().astype(np.uint8)
    
    # intensity 値をクリップしてから uint8 型に変換
    intensity_clipped = np.clip(intensity, 0, 255).round().astype(np.uint8)
    
    # label 値を int16 型に変換
    label_rounded = label.round().astype(np.int16)
    
    return x, y, z, red, green, blue, intensity_clipped, label_rounded

def shift_to_origin(x, y, z):
    centroid = np.mean(np.stack([x, y, z], axis=-1), axis=0)
    x -= centroid[0]
    y -= centroid[1]
    z -= centroid[2]
    return x, y, z


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process and optionally shift PLY/TXT files to origin.")
    parser.add_argument('--input', dest="input_filename", type=str, required=True, help="Input filename with extension")
    parser.add_argument("--output", dest="output_filename", type=str, required=True, help="Output PLY filename without extension")
    parser.add_argument("--shift_to_origin", action="store_true", help="Shift the point cloud so that its centroid is at the origin")
    
    args = parser.parse_args()
    
    filename, file_extension = os.path.splitext(args.input_filename)
    if file_extension.lower() == '.ply':
        x, y, z, red, green, blue, intensity, label = read_ply_and_adjust_data_types(args.input_filename)
    elif file_extension.lower() == '.txt':
        x, y, z, red, green, blue, intensity, label = read_txt_and_adjust_data_types(args.input_filename)
    else:
        raise ValueError("Unsupported file format: {}".format(file_extension))
    
    if args.shift_to_origin:
        x, y, z = shift_to_origin(x, y, z)
    
    save_ply(args.output_filename, x, y, z, red, green, blue, intensity, label)

#コマンド
#python plyv1.py --input example --output example_shifted --shift_to_origin

