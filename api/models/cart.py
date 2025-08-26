# carts.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

router = APIRouter(prefix="/carts", tags=["carts"])


# Crear carrito
@router.post("/")
def create_cart(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    new_cart = Cart(user_id=user_id)
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return {"id": new_cart.id, "user_id": new_cart.user_id}


# Agregar producto al carrito
@router.post("/{cart_id}/items/")
def add_item(cart_id: int, product_id: int, quantity: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="Stock insuficiente")

    new_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {
        "id": new_item.id,
        "cart_id": new_item.cart_id,
        "product_id": new_item.product_id,
        "quantity": new_item.quantity
    }


# Listar carrito con items
@router.get("/{cart_id}")
def get_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")

    items = db.query(CartItem).filter(CartItem.cart_id == cart_id).all()
    return {
        "id": cart.id,
        "user_id": cart.user_id,
        "items": [
            {
                "id": item.id,
                "product_id": item.product_id,
                "quantity": item.quantity
            } for item in items
        ]
    }


# Eliminar item del carrito
@router.delete("/{cart_id}/items/{item_id}")
def delete_item(cart_id: int, item_id: int, db: Session = Depends(get_db)):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    db.delete(item)
    db.commit()
    return {"detail": "Item eliminado correctamente"}


# Vaciar carrito
@router.delete("/{cart_id}/clear")
def clear_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")

    db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()
    db.commit()
    return {"detail": "Carrito vaciado correctamente"}
