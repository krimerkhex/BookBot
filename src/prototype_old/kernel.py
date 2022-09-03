# import dal
import gateway


try:
    gateway.bot.polling()
except Exception as ex:
    print("err: ", ex)

# chat_id = 273604991
# gateway.watch_all_bookings('KZN', chat_id)
