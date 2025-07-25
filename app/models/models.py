import uuid
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, List
from enum import Enum
from decimal import Decimal


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=100)
    email: str = Field(max_length=255)
    phone_number: str = Field(max_length=15)
    role: str = Field(max_length=5)
    created_at: datetime
    updated_at: datetime


class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Booking(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # Client information
    client_name: str = Field(max_length=255)
    email: str = Field(max_length=255)
    phone: Optional[str] = Field(default=None, max_length=20)

    # Booking details
    start_time: datetime
    end_time: datetime
    service_type: Optional[str] = Field(default=None, max_length=100)
    notes: Optional[str] = Field(default=None, max_length=1000)

    # Business information (if relevant)
    owner_name: str = Field(max_length=255)
    address: str = Field(max_length=255)

    # Status and management
    status: BookingStatus = Field(default=BookingStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Future user integration
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")

    # Pricing (if applicable)
    estimated_price: Optional[float] = Field(default=None)
    final_price: Optional[float] = Field(default=None)


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"  # cooking, preparing, processing
    READY = "ready"  # ready for pickup/delivery
    COMPLETED = "completed"  # delivered, picked up, or finished
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class OrderType(str, Enum):
    PICKUP = "pickup"
    DELIVERY = "delivery"
    DINE_IN = "dine_in"
    ONLINE = "online"
    IN_STORE = "in_store"
    SERVICE = "service"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class Order(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # Customer info (generic for any business)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")
    customer_name: str = Field(max_length=255)
    email: str = Field(max_length=255)
    phone_number: Optional[str] = Field(max_length=15)

    # Flexible address (could be delivery, shipping, or service location)
    address: Optional[str] = Field(max_length=255)
    city: Optional[str] = Field(max_length=255)
    state: Optional[str] = Field(max_length=100)
    postal_code: Optional[str] = Field(max_length=20)
    country: Optional[str] = Field(max_length=100, default="US")

    # Order details (flexible for any business type)
    order_type: OrderType = Field(default=OrderType.PICKUP)

    # Pricing (universal)
    subtotal: Decimal = Field(max_digits=10, decimal_places=2)
    tax_amount: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    service_fee: Decimal = Field(default=0, max_digits=10, decimal_places=2)  # delivery fee, service charge, etc.
    discount_amount: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    tip_amount: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    total_amount: Decimal = Field(max_digits=10, decimal_places=2)

    # Status tracking
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    payment_status: PaymentStatus = Field(default=PaymentStatus.PENDING)

    # Timestamps (universal)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    scheduled_for: Optional[datetime] = Field(default=None)  # pickup time, delivery time, appointment
    completed_at: Optional[datetime] = Field(default=None)

    # Flexible additional info
    special_instructions: Optional[str] = Field(max_length=1000)  # cooking notes, delivery instructions, etc.
    reference_number: Optional[str] = Field(max_length=100)  # table number, confirmation code, etc.

    # Payment info (universal)
    payment_method: Optional[str] = Field(max_length=50)
    payment_reference: Optional[str] = Field(max_length=100)

    # Business-specific flexibility
    promo_code: Optional[str] = Field(max_length=50)
    business_notes: Optional[str] = Field(max_length=1000)  # internal notes

    class Config:
        validate_assignment = True


# Separate table for order items (works for any business)
class OrderItem(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    order_id: uuid.UUID = Field(foreign_key="order.id")

    # Generic item info
    item_name: str = Field(max_length=255)  # product name, menu item, service name
    item_description: Optional[str] = Field(max_length=500)
    item_category: Optional[str] = Field(max_length=100)  # food category, product type, service type

    # Quantity and pricing
    quantity: int = Field(default=1, ge=1)
    unit_price: Decimal = Field(max_digits=10, decimal_places=2)
    total_price: Decimal = Field(max_digits=10, decimal_places=2)

    # Flexible customizations
    customizations: Optional[str] = Field(max_length=500)  # "extra cheese", "size large", "color red"
    item_notes: Optional[str] = Field(max_length=500)  # special requests for this item

    # SKU or reference (optional)
    item_reference: Optional[str] = Field(max_length=100)  # SKU, menu item ID, service code

    created_at: datetime = Field(default_factory=datetime.utcnow)