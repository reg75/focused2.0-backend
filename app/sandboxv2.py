@router.get("/teachers", response_model=List[Teachers_List])
def fetch_teachers(db: Session = Depends(get_db)):
   # EN: Fetch all 
   teachers = db.query(User).order_by(User.User_Surname).all()

   # EN: Return a message if there are no teachers found
   # BR: 
   if not teachers: 
      return {"message": "Error: No teachers found"}

   # EN: Return a list of teachers
   # BR: 
   return [
      Teachers_List(
         User_ID=teacher.User_ID,
         Teacher_Forename=teacher.User_Forename,
         Teacher_Surname=teacher.User_Surname,
         )
    for teacher in teachers
]
