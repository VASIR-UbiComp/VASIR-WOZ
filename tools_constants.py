from tools import *

tools = [
    {
        "type": "function",
        "function": {
            "name": "change_volume",
            "description": "Zmienia głośności mowy",
            "parameters": {
                "type": "object",
                "properties": {
                    "volume_level": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 10,
                        "default": 5,
                        "description": "Docelowy poziom głośności (od 1 do 10) dla pliku lub rozmowy. Domyślnie ustawione na 5.",
                    }
                },
                "required": ["volume_level"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_medicine",
            "description": "Dodaje lek do bazy danych.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Nazwa lekarstwa",
                    },
                    "pills_count": {
                        "type": "number",
                        "description": "Ilość tabletek, które należy przyjąć",
                    },
                    "when_to_take_day": {
                        "type": "array",
                        "description": "Dni tygodnia, w które należy przyjąć lek",
                        "items": {"type": "string"},
                    },
                    "when_to_take_hours": {
                        "type": "array",
                        "description": "Godziny, w których należy przyjąć lek",
                        "items": {"type": "integer", "minimum": 0, "maximum": 23},
                    },
                    "when_to_take_minutes": {
                        "type": "array",
                        "description": "Minuty, w których należy przyjąć lek",
                        "items": {"type": "number", "minimum": 0, "maximum": 59},
                    },
                },
                "required": [
                    "name",
                    "pills_count",
                    "when_to_take_day",
                    "when_to_take_hours",
                    "when_to_take_minutes",
                ],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_event",
            "description": "Adds an event to the calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {
                        "type": "integer",
                        "description": "The day of the event (1-31)."
                    },
                    "month": {
                        "type": "string",
                        "description": "The month of the event (e.g., 'January', 'February')."
                    },
                    "year": {
                        "type": "integer",
                        "description": "The year of the event."
                    },
                    "hour": {
                        "type": "integer",
                        "description": "The hour of the event (0-23)."
                    },
                    "minute": {
                        "type": "integer",
                        "description": "The minute of the event (0-59)."
                    },
                    "content": {
                        "type": "string",
                        "description": "A description or content of the event."
                    },
                    "reminders": {
                        "type": "array",
                        "description": "An array of reminder details for the event.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "days_before": {
                                    "type": "integer",
                                    "description": "The number of days before the event to set the reminder."
                                },
                                "hours_before": {
                                    "type": "integer",
                                    "description": "The number of hours before the event to set the reminder."
                                },
                                "minutes_before": {
                                    "type": "integer",
                                    "description": "The number of minutes before the event to set the reminder."
                                }
                            },
                            "required": ["days_before", "hours_before", "minutes_before"]
                        }
                    }
                },
                "required": ["day", "month", "year", "hour", "minute", "content", "reminders"]
            }
        }
    },
    #create_shopping_list
    {
    "type": "function",
    "function": {
        "name": "create_shopping_list",
        "description": "Tworzy nową listę zakupów z podaną nazwą i produktami. Sprawdza, czy lista o tej samej nazwie już istnieje.",
        "parameters": {
        "type": "object",
        "properties": {
            "name": {
            "type": "string",
            "description": "Nazwa listy zakupów, która ma zostać utworzona."
            },
            "products": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "Lista produktów, które mają być dodane do nowej listy zakupów."
            }
        },
        "required": ["name", "products"]
        }
    }
    },
    #add_to_shopping_list
    {
    "type": "function",
    "function": {
        "name": "add_to_shopping_list",
        "description": "Dodaje produkty do istniejącej listy zakupów o podanej nazwie. Sprawdza, czy lista o tej nazwie istnieje.",
        "parameters": {
        "type": "object",
        "properties": {
            "name": {
            "type": "string",
            "description": "Nazwa listy zakupów, do której mają zostać dodane produkty."
            },
            "products": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "Lista produktów, które mają zostać dodane do istniejącej listy zakupów."
            }
        },
        "required": ["name", "products"]
        }
    }
    },
    #delete_from_shopping_list
    {
    "type": "function",
    "function": {
        "name": "delete_from_shopping_list",
        "description": "Usuwa produkty z istniejącej listy zakupów o podanej nazwie. Sprawdza, czy lista o tej nazwie istnieje, a następnie usuwa podane produkty.",
        "parameters": {
        "type": "object",
        "properties": {
            "name": {
            "type": "string",
            "description": "Nazwa listy zakupów, z której mają zostać usunięte produkty."
            },
            "products": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "Lista produktów, które mają zostać usunięte z istniejącej listy zakupów."
            }
        },
        "required": ["name", "products"]
        }
    }
    },
    #list_all_shopping_lists
    {
    "type": "function",
    "function": {
        "name": "list_shopping_lists",
        "description": "Wyświetla dostępne listy zakupów wraz z przypisanymi do nich produktami. Jeśli nie ma żadnych list, informuje użytkownika o braku list.",
        "parameters": {
        "type": "object",
        "properties": {},
        "required": []
        }
    }
    },
    {
        "type": "function",
        "function": {
            "name": "set_monthly_budget",
            "description": "Ustala budżet na specyficzny miesiąc i rok",
            "parameters": {
                "type": "object",
                "properties": {
                    "month": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 12,
                        "description": "Miesiąc budżetu reprezentowany jako liczba całkowita od 1 do 12",
                    },
                    "year": {
                        "type": "integer",
                        "description": "Rok",
                    },
                    "amount": {
                        "type": "number",
                        "minimum": 0,
                        "description": "Wysokość budżetu na dany miesiąc",
                    },
                },
                "required": ["month", "year", "amount"],
            },
        },
    },
]

available_functions = {
    "change_volume": change_volume,
    "add_medicine": add_medicine,
    "add_event": add_event,
    "set_monthly_budget": set_monthly_budget,
    "add_spending": add_spending,
    "add_income": add_income,
    "add_recurring_spending": add_recurring_spending,
    "create_shopping_list": create_shopping_list,
    "add_to_shopping_list": add_to_shopping_list,
    "delete_from_shopping_list": delete_from_shopping_list,
    "list_shopping_lists": list_shopping_lists,
}
