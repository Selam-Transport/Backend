from fastapi import APIRouter, HTTPException, Depends
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate,TicketResponse
from app.config.database import ticket_collection
from app.routes.user import get_current_user

router = APIRouter()    


@router.post("/ticket", response_model=TicketResponse)  
async def create_ticket(ticket: TicketCreate, current_user: dict = Depends(get_current_user)):
    new_ticket = Ticket(**ticket.dict(), owner_id=current_user["id"])
    await  ticket_collection.insert_one(ticket.dict())
    return TicketResponse(**new_ticket.dic())


@router.get("/tickets/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: str, current_user: User = Depends(get_current_user)):
    ticket = await ticket_collection.find_one({"_id":ticket_id, "owner_id": current_user["id"]})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket is not found")
    return TicketResponse(**ticket)
    