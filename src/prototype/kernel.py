import gateway


def try_again():
    try:
        gateway.bot.polling()
    except Exception as ex:
        print("err: ", ex)
    finally:
        try_again()


if __name__ == '__main__':
    try_again()
