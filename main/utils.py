from math import radians, cos, sin, asin, sqrt, atan, tan, atan2

# The Haversine method to calculate the difference in distance
def haversine(lon1, lat1, lon2, lat2):
    R = 6372.8  # Radius of Earth in kilometers

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dLon / 2) ** 2
    c = 2 * asin(sqrt(a))

    return R * c

# Vincenty's formula for geodesic distance calculation
def vincenty_distance(lon1, lat1, lon2, lat2):
    a = 6378137.0  # Semi-major axis of the Earth (meters)
    f = 1 / 298.257223563  # Flattening
    b = (1 - f) * a  # Semi-minor axis

    # Convert degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # If the coordinates are identical, return 0 distance
    if lon1 == lon2 and lat1 == lat2:
        return 0.0

    L = lon2 - lon1
    U1 = atan((1 - f) * tan(lat1))
    U2 = atan((1 - f) * tan(lat2))

    sinU1, cosU1 = sin(U1), cos(U1)
    sinU2, cosU2 = sin(U2), cos(U2)

    lamb = L
    iter_limit = 100  # Maximum iterations for convergence

    while iter_limit > 0:
        sin_lambda, cos_lambda = sin(lamb), cos(lamb)
        sin_sigma = sqrt((cosU2 * sin_lambda) ** 2 + (cosU1 * sinU2 - sinU1 * cosU2 * cos_lambda) ** 2)
        
        # Prevent division by zero error
        if sin_sigma == 0:
            return 0.0  # Points are the same

        cos_sigma = sinU1 * sinU2 + cosU1 * cosU2 * cos_lambda
        sigma = atan2(sin_sigma, cos_sigma)

        sin_alpha = cosU1 * cosU2 * sin_lambda / sin_sigma
        cos2_alpha = 1 - sin_alpha ** 2
        cos2_sigma_m = cos_sigma - (2 * sinU1 * sinU2 / cos2_alpha) if cos2_alpha != 0 else 0

        C = (f / 16) * cos2_alpha * (4 + f * (4 - 3 * cos2_alpha))
        lamb_prev = lamb
        lamb = L + (1 - C) * f * sin_alpha * (
            sigma + C * sin_sigma * (cos2_sigma_m + C * cos_sigma * (-1 + 2 * cos2_sigma_m ** 2))
        )

        if abs(lamb - lamb_prev) < 1e-12:
            break  # Convergence reached

        iter_limit -= 1

    if iter_limit == 0:
        return None  # No convergence

    u2 = cos2_alpha * ((a ** 2 - b ** 2) / b ** 2)
    A = 1 + (u2 / 16384) * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    B = (u2 / 1024) * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))

    delta_sigma = B * sin_sigma * (cos2_sigma_m + (B / 4) * (cos_sigma * (-1 + 2 * cos2_sigma_m ** 2) - 
                    (B / 6) * cos2_sigma_m * (-3 + 4 * sin_sigma ** 2) * (-3 + 4 * cos2_sigma_m ** 2)))

    distance = b * A * (sigma - delta_sigma)  # Distance in meters
    return distance / 1000  # Convert to kilometers
