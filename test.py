#dict = {}
dict = {'name': [1], 'val': [1]}



face_descriptor_name = dict.get('name')
face_descriptor_it = dict.get('val')


#print(face_descriptor_name)
#print(face_descriptor_it)

face_descriptor_it.append(9)
face_descriptor_name.append(2)
face_descriptor_it.append(7)
face_descriptor_name.append(3)
face_descriptor_it.append(6)
face_descriptor_name.append(8)

print(dict.get('name')[-1])