from others.Udiq import UdiqController, Knowledge
import Config

udiq_controller = UdiqController(Config.MONGODB_URI, "discord", "udiq", print)

print(udiq_controller.get_udiq())

udiq_controller.append_record("test", "テスト")

k = Knowledge("ユビキタス2", "共通言語")
udiq_controller.update_db_udiq_record(k)

udiq_controller.delete_db_udiq_record(k.word)