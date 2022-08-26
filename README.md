### Эксперименты с NATS

Небольшие практические примеры работы с системой сообщений [NATS](https://nats.io/). Все примеры исходного кода идут попарно, публикатор + подписчик.  

Перед началом работы необходимо [установить](https://nats.io/download/) и запустить сервер NATS:
```
REM Windows:
nats-server.exe -js REM Start NATS Server with JetStream
nats account info REM Check JetStream status
```
```
# Linux:
sudo nats-server -js # Start NATS Server with JetStream
nats account info # Check JetStream status
```

Также необходимо установить пакет _nats-py_:
```
pip install nats-py
```

Всего в этом репозитарии 8 примеров работы с NATS, описанных ниже.
```mermaid
  graph TD;
      A(1. Basic example)-->B(2. Auth with credentials);
      A-->C(3. Work with JetStream);
      C-->D(4. Add callbacks and exception handling);
      D-->E(5. Work with Key/Value Store);
      E-->F(6. Work with token)
      D-->G(7. Extract NATS connector class)
      G-->H(8. Add logger)
```

1. Простейший пример.  
Строку подключения
```
nats_connector = await nats.connect(servers=["nats://localhost:4222"],
                                        name="NATS simple example publisher",
                                        connect_timeout=10,
                                        ping_interval=20,
                                        max_outstanding_pings=6,
                                        allow_reconnect=True,
                                        dont_randomize=False,
                                        reconnect_time_wait=5,
                                        no_echo=False)
```
в пределе можно сократить до
```
nats_connector = await nats.connect("nats://localhost:4222")
```
  
2. Авторизация на сервере при помощи файла сертификата ([credentials](https://docs.nats.io/using-nats/developer/connecting/creds)).

3. Пример работы с [JetStream](https://docs.nats.io/nats-concepts/jetstream), буферным хранилищем, позволяющим хранить непрочитанные сообщения на диске или в оперативной памяти.

4. Добавляем обработку исключений и функции обратного вызова.

5. Пример работы с [Key/Value Store](https://docs.nats.io/using-nats/developer/develop_jetstream/kv), надстройки над JetStream, позволяющей организовать более упорядоченное хранение информации.

6. Key/Value Store + авторизация по [токену](https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro/tokens).

7. Функционал работы с NATS выделен в отдельный класс.

8. Добавлен логгер для вывода логов как в консоль (colorlog), так и в файл (RotatingFileHandler).

Ветка с примерами 5 и 6 не совсем полноценна, потому что разработчики NATS до сих пор не реализовали функционал подписки на Key/Value хранилища (т. н. watch()), поэтому подписчик фактически вынужден "вручную" забирать данные при помощи get(), поэтому я бы рекомендовал для практической работы пример № 8 (на базе JetStream).