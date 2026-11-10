from lab6.booking import booking_allowed


def test_open_trip_with_one_seat_is_allowed():
    # Arrange: Нээлттэй аялалд гурван сул суудал байна.
    requested, available, status = 1, 3, "OPEN"

    # Act: Нэг суудал авах боломжийг шалгана.
    result = booking_allowed(requested, available, status)

    # Assert: Захиалга зөвшөөрөгдөнө.
    assert result is True


def test_open_trip_with_multiple_seats_is_allowed():
    # Arrange
    requested, available, status = 2, 5, "OPEN"

    # Act
    result = booking_allowed(requested, available, status)

    # Assert
    assert result is True


def test_zero_requested_seats_is_rejected():
    # Arrange: Зөвшөөрөгдөх доод хязгаараас бага утга.
    requested, available, status = 0, 3, "OPEN"

    # Act
    result = booking_allowed(requested, available, status)

    # Assert
    assert result is False


def test_request_equal_to_capacity_is_allowed():
    # Arrange: Хүссэн суудал сул суудлын тоотой тэнцүү.
    requested, available, status = 3, 3, "OPEN"

    # Act
    result = booking_allowed(requested, available, status)

    # Assert
    assert result is True


def test_request_one_over_capacity_is_rejected():
    # Arrange
    requested, available, status = 4, 3, "OPEN"

    # Act
    result = booking_allowed(requested, available, status)

    # Assert
    assert result is False


def test_closed_trip_is_rejected():
    # Arrange: Суудал хүрэлцээтэй ч аялал хаалттай.
    requested, available, status = 1, 3, "CLOSED"

    # Act
    result = booking_allowed(requested, available, status)

    # Assert
    assert result is False