import os

def merge_obj_files(file_list, output_file):
    # Initializations
    vertices = []
    faces = []
    vertex_offset = 0

    for file in file_list:
        with open(file, 'r') as f:
            for line in f:
                if line.startswith('v '):  # Vertex definition
                    vertices.append(line.strip('\n') + ' 0.5 0.0 0.0' + '\n')
                elif line.startswith('f '):  # Face definition
                    # Update the face indices based on the current vertex offset
                    face_vertices = line.strip().split()[1:]
                    updated_face = 'f ' + ' '.join(
                        str(int(vertex.split('/')[0]) + vertex_offset) + ('/' + '/'.join(vertex.split('/')[1:]) if '/' in vertex else '')
                        for vertex in face_vertices
                    ) + '\n'
                    faces.append(updated_face)

            # Update the vertex offset for the next file
            vertex_offset += len([line for line in open(file) if line.startswith('v ')])

    # Write to the output file
    with open(output_file, 'w') as f:
        f.writelines(vertices)
        f.writelines(faces)

folder_path = 'heart/parts'
files_to_merge = []
for file_name in os.listdir(folder_path):
    files_to_merge.append(os.path.join(folder_path, file_name))
output_file = 'heart.obj'
merge_obj_files(files_to_merge, output_file)
