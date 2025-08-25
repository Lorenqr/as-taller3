from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.database import get_db
from api.models.cart import Cart, CartItem
from api.models.user import User
from api.models.product import Product

router = APIRouter()


USER_ID = 1


@router.get("/")
async def get_user_cart(db: Session = Depends(get_db)):
    # TODO: Implementar obtener carrito del usuario
    cart = db.query(Cart).filter(Cart.user_id == USER_ID).first()
    if not cart:
        cart = Cart(user_id=USER_ID)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return {"cart_id": cart.id, "items": cart.items}


@router.post("/items")
async def add_item_to_cart(product_id: int, quantity: int, db: Session = Depends(get_db)):
    # TODO: Implementar agregar item al carrito
    cart = db.query(Cart).filter(Cart.user_id == USER_ID).first()
    if not cart:
        cart = Cart(user_id=USER_ID)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id).first()
    if item:
        item.quantity += quantity
    else:
        item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.add(item)

    db.commit()
    db.refresh(item)
    return {"message": "Producto agregado al carrito", "item": item}


@router.put("/items/{item_id}")
async def update_cart_item(item_id: int, quantity: int, db: Session = Depends(get_db)):
    # TODO: Implementar actualizar cantidad de item
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")

    if quantity <= 0:
        db.delete(item)
        db.commit()
        return {"message": "Item eliminado porque la cantidad era <= 0"}

    item.quantity = quantity
    db.commit()
    db.refresh(item)
    return {"message": "Item actualizado", "item": item}


@router.delete("/items/{item_id}")
async def remove_item_from_cart(item_id: int, db: Session = Depends(get_db)):
    # TODO: Implementar remover item del carrito
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")

    db.delete(item)
    db.commit()
    return {"message": "Item eliminado del carrito"}


@router.delete("/")
async def clear_cart(db: Session = Depends(get_db)):
    # TODO: Implementar limpiar carrito
    cart = db.query(Cart).filter(Cart.user_id == USER_ID).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado")

    for item in cart.items:
        db.delete(item)

    db.commit()
    return {"message": "Carrito vaciado correctamente"}
