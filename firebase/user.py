def get_allergies(db, user_id):
    ref = db.collection(u'users').document((user_id))
    allergies = ref.get().to_dict()['allergies']
    return allergies

def add_allergy(db, user_id, allergy):
    ref = db.collection(u'users').document((user_id))
    allergies = ref.get().to_dict()['allergies']
    allergies.append(allergy)
    ref.update({u'allergies': allergies})
    return allergies

def remove_allergy(db, user_id, allergy):
    ref = db.collection(u'users').document((user_id))
    allergies = ref.get().to_dict()['allergies']
    if allergy in allergies:
        allergies.remove(allergy) 
    ref.update({u'allergies': allergies})
    return allergies