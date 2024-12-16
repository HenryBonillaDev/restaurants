import uuid
from celery import shared_task
from users.models import User
from restaurants.domain.models import Restaurant


def is_valid_uuid(value):
    try:
        if value in ["nan", None]:
            return None
        return uuid.UUID(value)
    except ValueError:
        return None


@shared_task
def import_users_task(users_data):
    success_count = 0
    error_messages = []

    for user_data in users_data:
        restaurant_id = user_data.get("restaurant_id")
        restaurant = None
        restaurant_id = is_valid_uuid(restaurant_id)

        if restaurant_id:
            try:
                restaurant = Restaurant.objects.get(id=restaurant_id)
            except Restaurant.DoesNotExist:
                error_messages.append(
                    f"Restaurant with ID {restaurant_id} does not exist."
                )
                continue

        try:
            user = User.objects.create_user(
                username=user_data["username"],
                password=user_data["password"],
                email=user_data["email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                phone=user_data["phone"],
                default_address=user_data["default_address"],
                role=user_data["role"],
                restaurant=restaurant,
            )
            user.save()
            success_count += 1
        except Exception as e:
            error_messages.append(
                f"Error processing user {user_data['username']}: {str(e)}"
            )
            continue

    return {
        "status": "completed with errors" if error_messages else "success",
        "success_count": success_count,
        "errors": error_messages,
    }
