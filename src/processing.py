def filter_by_state(data, state="EXECUTED"):
    """
    Фильтрует список транзакций по указанному статусу.

    Args:
        data (list): список транзакций (словарей);
        state (str): статус для фильтрации (по умолчанию "EXECUTED").

    Returns:
        list: отфильтрованный список транзакций с указанным статусом.
    """
    if not isinstance(data, list):
        return []

    filtered_data = []
    for transaction in data:
        if isinstance(transaction, dict) and transaction.get("state") == state:
            filtered_data.append(transaction)

    return filtered_data



def sort_by_date(data, reverse=False):
    """
    Сортирует транзакции по дате (от старых к новым или наоборот).

    Args:
        data (list): список транзакций (словарей) с полем 'date';
        reverse (bool): если True — сортировка от новых к старым (по умолчанию False).

    Returns:
        list: отсортированный список транзакций.
    """
    if not isinstance(data, list):
        return []

    # Фильтруем транзакции, у которых есть поле 'date'
    valid_transactions = [
        transaction for transaction in data
        if isinstance(transaction, dict) and "date" in transaction
    ]

    # Сортируем по полю 'date' (строки в формате ISO корректно сортируются лексикографически)
    sorted_data = sorted(
        valid_transactions,
        key=lambda x: x["date"],
        reverse=reverse
    )

    return sorted_data