workspace {
    name "Delivery Service"
    description "Моделирование архитектуры сервиса доставки"

    model {
        user = person "Пользователь" {
            description "Пользователь сервиса доставки"
        }

        delivery_service = softwareSystem "Сервис доставки" {
            description "Онлайн сервис для управления доставкой посылок"
            user -> this "Использует"

            web_app = container "Веб-приложение" {
                description "Интерфейс для пользователей сервиса доставки"
                technology "React"
                user -> this "Работает через"
            }

            api = container "API" {
                description "Backend API для управления пользователями, посылками и доставками"
                technology "Spring Boot"
                web_app -> this "Использует"
            }

            user_db = container "База данных пользователей" {
                description "Хранение данных пользователей"
                technology "PostgreSQL"
                api -> this "Читает и записывает"
            }

            parcel_db = container "База данных посылок" {
                description "Хранение информации о посылках"
                technology "PostgreSQL"
                api -> this "Читает и записывает"
            }

            delivery_db = container "База данных доставок" {
                description "Хранение информации о доставках"
                technology "PostgreSQL"
                api -> this "Читает и записывает"
            }
        }

        # Определение связей API
        user -> api "Создание нового пользователя"
        user -> api "Поиск пользователя по логину"
        user -> api "Поиск пользователя по имени и фамилии"
        user -> api "Создание посылки"
        user -> api "Получение списка посылок"
        user -> api "Создание доставки"
        user -> api "Получение информации о доставке"
    }

    views {
        systemContext delivery_service "Context" {
            include *
            autoLayout
        }

        container delivery_service "Containers" {
            include *
            autoLayout
        }

        dynamic delivery_service "Dynamic_CreateParcel" {
            autoLayout lr
            description "Сценарий создания посылки"

            user -> web_app "Открывает веб-приложение"
            web_app -> api "Запрос на создание посылки"
            api -> parcel_db "Сохранение данных о новой посылке"
        }

        styles {
            element "Person" {
                color #ffffff
                fontSize 22
                shape Person
            }
            element "Container" {
                background #438dd5
                color #ffffff
            }
            element "Database" {
                shape Cylinder
            }
        }
    }
}