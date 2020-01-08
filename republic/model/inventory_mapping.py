from typing import Dict, List, Union

def get_inventory_by_num(inventory_num: int) -> dict:
    for inv_map in inventory_mapping:
        if inv_map["inventory_num"] == inventory_num:
            return inv_map


def get_inventories_by_year(inventory_years: Union[int, List[int]]) -> list:
    if isinstance(inventory_years, int):
        inventory_years = [inventory_years]
    return [inv_map for inv_map in inventory_mapping if inv_map["year"] in inventory_years]


inventory_mapping = [
    {"inventory_num": 3174, "year": 1615},
    {"inventory_num": 3175, "year": 1616},
    {"inventory_num": 3176, "year": 1617},
    {"inventory_num": 3177, "year": 1618},
    {"inventory_num": 3178, "year": 1619},
    {"inventory_num": 3179, "year": 1620},
    {"inventory_num": 3180, "year": 1621},
    {"inventory_num": 3181, "year": 1622},
    {"inventory_num": 3182, "year": 1623},
    {"inventory_num": 3183, "year": 1624},
    {"inventory_num": 3184, "year": 1625},
    {"inventory_num": 3185, "year": 1626},
    {"inventory_num": 3186, "year": 1627},
    {"inventory_num": 3187, "year": 1628},
    {"inventory_num": 3188, "year": 1629},
    {"inventory_num": 3189, "year": 1630},
    {"inventory_num": 3190, "year": 1631},
    {"inventory_num": 3191, "year": 1632},
    {"inventory_num": 3192, "year": 1633},
    {"inventory_num": 3193, "year": 1634},
    {"inventory_num": 3194, "year": 1635},
    {"inventory_num": 3195, "year": 1636},
    {"inventory_num": 3196, "year": 1637},
    {"inventory_num": 3197, "year": 1638},
    {"inventory_num": 3198, "year": 1639},
    {"inventory_num": 3199, "year": 1640},
    {"inventory_num": 3200, "year": 1641},
    {"inventory_num": 3201, "year": 1642},
    {"inventory_num": 3202, "year": 1643},
    {"inventory_num": 3203, "year": 1644},
    {"inventory_num": 3204, "year": 1645},
    {"inventory_num": 3205, "year": 1646},
    {"inventory_num": 3206, "year": 1647},
    {"inventory_num": 3207, "year": 1648},
    {"inventory_num": 3208, "year": 1649, "period": ["1649-01-02", "1649-07-12"]},
    {"inventory_num": 3209, "year": 1649, "period": ["1649-07-12", "1649-12-31"]},
    {"inventory_num": 3210, "year": 1650},
    {"inventory_num": 3211, "year": 1651},
    {"inventory_num": 3212, "year": 1652, "period": ["1652-01-02", "1652-06-29"]},
    {"inventory_num": 3213, "year": 1652, "period": ["1652-07-01", "1652-12-31"]},
    {"inventory_num": 3214, "year": 1653, "period": ["1653-01-02", "1653-06-30"]},
    {"inventory_num": 3215, "year": 1653, "period": ["1653-07-01", "1653-12-31"]},
    {"inventory_num": 3216, "year": 1654},
    {"inventory_num": 3217, "year": 1655},
    {"inventory_num": 3218, "year": 1656},
    {"inventory_num": 3219, "year": 1657},
    {"inventory_num": 3220, "year": 1658},
    {"inventory_num": 3221, "year": 1659},
    {"inventory_num": 3222, "year": 1660},
    {"inventory_num": 3223, "year": 1661},
    {"inventory_num": 3224, "year": 1662},
    {"inventory_num": 3225, "year": 1663, "period": ["1663-01-02", "1663-06-30"]},
    {"inventory_num": 3226, "year": 1663, "period": ["1663-07-02", "1663-12-31"]},
    {"inventory_num": 3227, "year": 1664},
    {"inventory_num": 3228, "year": 1665, "period": ["1665-01-02", "1665-06-20"]},
    {"inventory_num": 3229, "year": 1665, "period": ["1665-07-02", "1665-09-30"]},
    {"inventory_num": 3230, "year": 1665, "period": ["1665-09-30", "1665-12-31"]},
    {"inventory_num": 3231, "year": 1666, "period": ["1666-01-01", "1666-06-29"]},
    {"inventory_num": 3232, "year": 1666, "period": ["1666-07-01", "1666-12-31"]},
    {"inventory_num": 3233, "year": 1667, "period": ["1667-01-03", "1667-06-30"]},
    {"inventory_num": 3234, "year": 1667, "period": ["1667-07-01", "1667-12-31"]},
    {"inventory_num": 3235, "year": 1668, "period": ["1668-01-02", "1668-06-30"]},
    {"inventory_num": 3236, "year": 1668, "period": ["1668-07-02", "1668-12-31"]},
    {"inventory_num": 3237, "year": 1669, "period": ["1669-01-02", "1669-06-29"]},
    {"inventory_num": 3238, "year": 1669, "period": ["1669-07-01", "1669-12-31"]},
    {"inventory_num": 3239, "year": 1670, "period": ["1670-01-02", "1670-06-30"]},
    {"inventory_num": 3240, "year": 1670, "period": ["1670-07-01", "1670-12-31"]},
    {"inventory_num": 3241, "year": 1671, "period": ["1671-01-02", "1671-06-30"]},
    {"inventory_num": 3242, "year": 1671, "period": ["1671-07-01", "1671-12-31"]},
    {"inventory_num": 3243, "year": 1672, "period": ["1e helft"]},
    {'inventory_num': 3244, 'period': ['1638-01-01', '1638-12-31'], 'year': 1638},
    {'inventory_num': 3245, 'period': ['1639-01-01', '1639-12-31'], 'year': 1639},
    {'inventory_num': 3246, 'period': ['1640-01-01', '1640-12-31'], 'year': 1640},
    {'inventory_num': 3247, 'period': ['1641-01-01', '1641-12-31'], 'year': 1641},
    {'inventory_num': 3248, 'period': ['1642-01-01', '1642-12-31'], 'year': 1642},
    {'inventory_num': 3249, 'period': ['1643-01-01', '1643-12-31'], 'year': 1643},
    {'inventory_num': 3250, 'period': ['1644-01-01', '1644-12-31'], 'year': 1644},
    {'inventory_num': 3251, 'period': ['1645-01-01', '1645-12-31'], 'year': 1645},
    {'inventory_num': 3252, 'period': ['1646-01-01', '1646-12-31'], 'year': 1646},
    {'inventory_num': 3253, 'period': ['1647-01-01', '1647-12-31'], 'year': 1647},
    {'inventory_num': 3254, 'period': ['1648-01-01', '1648-12-31'], 'year': 1648},
    {'inventory_num': 3255, 'period': ['1649-01-01', '1649-12-31'], 'year': 1649},
    {'inventory_num': 3256, 'period': ['1650-01-01', '1650-12-31'], 'year': 1650},
    {'inventory_num': 3257, 'period': ['1651-01-01', '1651-12-31'], 'year': 1651},
    {'inventory_num': 3258, 'period': ['1652-01-01', '1652-12-31'], 'year': 1652},
    {'inventory_num': 3259, 'period': ['1653-01-01', '1653-12-31'], 'year': 1653},
    {'inventory_num': 3260, 'period': ['1654-01-01', '1654-12-31'], 'year': 1654},
    {'inventory_num': 3261, 'period': ['1655-01-01', '1655-12-31'], 'year': 1655},
    {'inventory_num': 3262, 'period': ['1656-01-01', '1656-12-31'], 'year': 1656},
    {'inventory_num': 3263, 'period': ['1657-01-01', '1657-12-31'], 'year': 1657},
    {'inventory_num': 3264, 'period': ['1658-01-01', '1658-12-31'], 'year': 1658},
    {'inventory_num': 3265, 'period': ['1659-01-01', '1659-12-31'], 'year': 1659},
    {'inventory_num': 3266, 'period': ['1660-01-01', '1660-12-31'], 'year': 1660},
    {'inventory_num': 3267, 'period': ['1661-01-01', '1661-12-31'], 'year': 1661},
    {'inventory_num': 3268, 'period': ['1662-01-01', '1662-12-31'], 'year': 1662},
    {'inventory_num': 3269, 'period': ['1663-01-01', '1663-12-31'], 'year': 1663},
    {'inventory_num': 3270, 'period': ['1664-01-01', '1664-12-31'], 'year': 1664},
    {'inventory_num': 3271, 'period': ['1665-01-01', '1665-06-30'], 'year': 1665},
    {'inventory_num': 3272, 'period': ['1665-07-01', '1665-12-31'], 'year': 1665},
    {'inventory_num': 3273, 'period': ['1666-01-01', '1666-06-30'], 'year': 1666},
    {'inventory_num': 3274, 'period': ['1666-07-01', '1666-12-31'], 'year': 1666},
    {'inventory_num': 3275, 'period': ['1667-01-01', '1667-06-30'], 'year': 1667},
    {'inventory_num': 3276, 'period': ['1667-07-01', '1667-12-31'], 'year': 1667},
    {'inventory_num': 3277, 'period': ['1668-01-01', '1668-06-30'], 'year': 1668},
    {'inventory_num': 3278, 'period': ['1668-07-01', '1668-12-31'], 'year': 1668},
    {'inventory_num': 3279, 'period': ['1669-01-01', '1669-06-30'], 'year': 1669},
    {'inventory_num': 3280, 'period': ['1669-07-01', '1669-12-31'], 'year': 1669},
    {'inventory_num': 3281, 'period': ['1670-01-01', '1670-06-30'], 'year': 1670},
    {'inventory_num': 3282, 'period': ['1670-07-01', '1670-12-31'], 'year': 1670},
    {'inventory_num': 3283, 'period': ['1671-01-01', '1671-06-30'], 'year': 1671},
    {'inventory_num': 3284, 'period': ['1671-07-01', '1671-12-31'], 'year': 1671},
    {'inventory_num': 3285, 'period': ['1672-01-01', '1672-06-30'], 'year': 1672},
    {'inventory_num': 3286, 'period': ['1672-07-01', '1672-12-31'], 'year': 1672},
    {'inventory_num': 3287, 'period': ['1673-01-01', '1673-06-30'], 'year': 1673},
    {'inventory_num': 3288, 'period': ['1673-07-01', '1673-12-31'], 'year': 1673},
    {'inventory_num': 3289, 'period': ['1674-01-01', '1674-06-30'], 'year': 1674},
    {'inventory_num': 3290, 'period': ['1674-07-01', '1674-12-31'], 'year': 1674},
    {'inventory_num': 3291, 'period': ['1675-01-01', '1675-06-30'], 'year': 1675},
    {'inventory_num': 3292, 'period': ['1675-07-01', '1675-12-31'], 'year': 1675},
    {'inventory_num': 3293, 'period': ['1676-01-01', '1676-06-30'], 'year': 1676},
    {'inventory_num': 3294, 'period': ['1676-07-01', '1676-12-31'], 'year': 1676},
    {'inventory_num': 3295, 'period': ['1677-01-01', '1677-06-30'], 'year': 1677},
    {'inventory_num': 3296, 'period': ['1677-07-01', '1677-12-31'], 'year': 1677},
    {'inventory_num': 3297, 'period': ['1678-01-01', '1678-06-30'], 'year': 1678},
    {'inventory_num': 3298, 'period': ['1678-07-01', '1678-12-31'], 'year': 1678},
    {'inventory_num': 3299, 'period': ['1679-01-01', '1679-06-30'], 'year': 1679},
    {'inventory_num': 3300, 'period': ['1679-07-01', '1679-12-31'], 'year': 1679},
    {'inventory_num': 3301, 'period': ['1680-01-01', '1680-06-30'], 'year': 1680},
    {'inventory_num': 3302, 'period': ['1680-07-01', '1680-12-31'], 'year': 1680},
    {'inventory_num': 3303, 'period': ['1681-01-01', '1681-06-30'], 'year': 1681},
    {'inventory_num': 3304, 'period': ['1681-07-01', '1681-12-31'], 'year': 1681},
    {'inventory_num': 3305, 'period': ['1682-01-01', '1682-06-30'], 'year': 1682},
    {'inventory_num': 3306, 'period': ['1682-07-01', '1682-12-31'], 'year': 1682},
    {'inventory_num': 3307, 'period': ['1683-01-01', '1683-06-30'], 'year': 1683},
    {'inventory_num': 3308, 'period': ['1683-07-01', '1683-12-31'], 'year': 1683},
    {'inventory_num': 3309, 'period': ['1684-01-01', '1684-06-30'], 'year': 1684},
    {'inventory_num': 3310, 'period': ['1684-07-01', '1684-12-31'], 'year': 1684},
    {'inventory_num': 3311, 'period': ['1685-01-01', '1685-06-30'], 'year': 1685},
    {'inventory_num': 3312, 'period': ['1685-07-01', '1685-12-31'], 'year': 1685},
    {'inventory_num': 3313, 'period': ['1686-01-01', '1686-06-30'], 'year': 1686},
    {'inventory_num': 3314, 'period': ['1686-07-01', '1686-12-31'], 'year': 1686},
    {'inventory_num': 3315, 'period': ['1687-01-01', '1687-06-30'], 'year': 1687},
    {'inventory_num': 3316, 'period': ['1687-07-01', '1687-12-31'], 'year': 1687},
    {'inventory_num': 3317, 'period': ['1688-01-01', '1688-06-30'], 'year': 1688},
    {'inventory_num': 3318, 'period': ['1688-07-01', '1688-12-31'], 'year': 1688},
    {'inventory_num': 3319, 'period': ['1689-01-01', '1689-06-30'], 'year': 1689},
    {'inventory_num': 3320, 'period': ['1689-07-01', '1689-12-31'], 'year': 1689},
    {'inventory_num': 3321, 'period': ['1690-01-01', '1690-06-30'], 'year': 1690},
    {'inventory_num': 3322, 'period': ['1690-07-01', '1690-12-31'], 'year': 1690},
    {'inventory_num': 3323, 'period': ['1691-01-01', '1691-06-30'], 'year': 1691},
    {'inventory_num': 3324, 'period': ['1691-07-01', '1691-12-31'], 'year': 1691},
    {'inventory_num': 3325, 'period': ['1692-01-01', '1692-06-30'], 'year': 1692},
    {'inventory_num': 3326, 'period': ['1692-07-01', '1692-12-31'], 'year': 1692},
    {'inventory_num': 3327, 'period': ['1693-01-01', '1693-06-30'], 'year': 1693},
    {'inventory_num': 3328, 'period': ['1693-07-01', '1693-12-31'], 'year': 1693},
    {'inventory_num': 3329, 'period': ['1694-01-01', '1694-06-30'], 'year': 1694},
    {'inventory_num': 3330, 'period': ['1694-07-01', '1694-12-31'], 'year': 1694},
    {'inventory_num': 3331, 'period': ['1695-01-01', '1695-06-30'], 'year': 1695},
    {'inventory_num': 3332, 'period': ['1695-07-01', '1695-12-31'], 'year': 1695},
    {'inventory_num': 3333, 'period': ['1696-01-01', '1696-06-30'], 'year': 1696},
    {'inventory_num': 3334, 'period': ['1696-07-01', '1696-12-31'], 'year': 1696},
    {'inventory_num': 3335, 'period': ['1697-01-01', '1697-06-30'], 'year': 1697},
    {'inventory_num': 3336, 'period': ['1697-07-01', '1697-12-31'], 'year': 1697},
    {'inventory_num': 3337, 'period': ['1698-01-01', '1698-06-30'], 'year': 1698},
    {'inventory_num': 3338, 'period': ['1698-07-01', '1698-12-31'], 'year': 1698},
    {'inventory_num': 3339, 'period': ['1699-01-01', '1699-06-30'], 'year': 1699},
    {'inventory_num': 3340, 'period': ['1699-07-01', '1699-12-31'], 'year': 1699},
    {'inventory_num': 3341, 'period': ['1700-01-01', '1700-06-30'], 'year': 1700},
    {'inventory_num': 3342, 'period': ['1700-07-01', '1700-12-31'], 'year': 1700},
    {'inventory_num': 3344, 'period': ['1701-01-01', '1701-06-30'], 'year': 1701},
    {'inventory_num': 3345, 'period': ['1701-07-01', '1701-12-31'], 'year': 1701},
    {'inventory_num': 3346, 'period': ['1702-01-01', '1702-06-30'], 'year': 1702},
    {'inventory_num': 3347, 'period': ['1702-07-01', '1702-12-31'], 'year': 1702},
    {"inventory_num": 3760, "year": 1705, "period": ["1705-01-01", "1705-12-31"]},
    {"inventory_num": 3761, "year": 1706, "period": ["1706-01-01", "1706-12-31"]},
    {"inventory_num": 3762, "year": 1707, "period": ["1707-01-01", "1707-12-31"]},
    {"inventory_num": 3763, "year": 1708, "period": ["1708-01-01", "1708-12-31"]},
    {"inventory_num": 3764, "year": 1709, "period": ["1709-01-01", "1709-12-31"]},
    {"inventory_num": 3765, "year": 1710, "period": ["1710-01-01", "1710-12-31"]},
    {"inventory_num": 3766, "year": 1711, "period": ["1711-01-01", "1711-12-31"]},
    {"inventory_num": 3767, "year": 1712, "period": ["1712-01-01", "1712-12-31"]},
    {"inventory_num": 3768, "year": 1713, "period": ["1713-01-01", "1713-12-31"]},
    {"inventory_num": 3769, "year": 1714, "period": ["1714-01-01", "1714-12-31"]},
    {"inventory_num": 3770, "year": 1715, "period": ["1715-01-01", "1715-12-31"]},
    {"inventory_num": 3771, "year": 1716, "period": ["1716-01-01", "1716-12-31"]},
    {"inventory_num": 3772, "year": 1717, "period": ["1717-01-01", "1717-12-31"]},
    {"inventory_num": 3773, "year": 1718, "period": ["1718-01-01", "1718-12-31"]},
    {"inventory_num": 3774, "year": 1719, "period": ["1719-01-01", "1719-12-31"]},
    {"inventory_num": 3775, "year": 1720, "period": ["1720-01-01", "1720-12-31"]},
    {"inventory_num": 3776, "year": 1721, "period": ["1721-01-01", "1721-12-31"]},
    {"inventory_num": 3777, "year": 1722, "period": ["1722-01-01", "1722-12-31"]},
    {"inventory_num": 3778, "year": 1723, "period": ["1723-01-01", "1723-12-31"]},
    {"inventory_num": 3779, "year": 1724, "period": ["1724-01-01", "1724-12-31"]},
    {"inventory_num": 3780, "year": 1725, "period": ["1725-01-01", "1725-12-31"]},
    {"inventory_num": 3781, "year": 1726, "period": ["1726-01-01", "1726-12-31"]},
    {"inventory_num": 3782, "year": 1727, "period": ["1727-01-01", "1727-12-31"]},
    {"inventory_num": 3783, "year": 1728, "period": ["1728-01-01", "1728-12-31"]},
    {"inventory_num": 3784, "year": 1729, "period": ["1729-01-01", "1729-12-31"]},
    {"inventory_num": 3785, "year": 1730, "period": ["1730-01-01", "1730-12-31"]},
    {"inventory_num": 3786, "year": 1731, "period": ["1731-01-01", "1731-12-31"]},
    {"inventory_num": 3787, "year": 1732, "period": ["1732-01-01", "1732-12-31"]},
    {"inventory_num": 3788, "year": 1733, "period": ["1733-01-01", "1733-12-31"]},
    {"inventory_num": 3789, "year": 1734, "period": ["1734-01-01", "1734-12-31"]},
    {"inventory_num": 3790, "year": 1735, "period": ["1735-01-01", "1735-12-31"]},
    {"inventory_num": 3791, "year": 1736, "period": ["1736-01-01", "1736-12-31"]},
    {"inventory_num": 3792, "year": 1737, "period": ["1737-01-01", "1737-12-31"]},
    {"inventory_num": 3793, "year": 1738, "period": ["1738-01-01", "1738-12-31"]},
    {"inventory_num": 3794, "year": 1739, "period": ["1739-01-01", "1739-12-31"]},
    {"inventory_num": 3795, "year": 1740, "period": ["1740-01-01", "1740-12-31"]},
    {"inventory_num": 3796, "year": 1741, "period": ["1741-01-01", "1741-12-31"]},
    {"inventory_num": 3797, "year": 1742, "period": ["1742-01-01", "1742-12-31"]},
    {"inventory_num": 3798, "year": 1743, "period": ["1743-01-01", "1743-12-31"]},
    {"inventory_num": 3799, "year": 1744, "period": ["1744-01-01", "1744-12-31"]},
    {"inventory_num": 3800, "year": 1745, "period": ["1745-01-01", "1745-12-31"]},
    {"inventory_num": 3801, "year": 1746, "period": ["1746-01-01", "1746-12-31"]},
    {"inventory_num": 3802, "year": 1747, "period": ["1747-01-01", "1747-12-31"]},
    {"inventory_num": 3803, "year": 1748, "period": ["1748-01-01", "1748-12-31"]},
    {"inventory_num": 3804, "year": 1749, "period": ["1749-01-01", "1749-12-31"]},
    {"inventory_num": 3805, "year": 1750, "period": ["1750-01-01", "1750-12-31"]},
    {"inventory_num": 3806, "year": 1751, "period": ["1751-01-01", "1751-12-31"]},
    {"inventory_num": 3807, "year": 1752, "period": ["1752-01-01", "1752-12-31"]},
    {"inventory_num": 3808, "year": 1753, "period": ["1753-01-01", "1753-12-31"]},
    {"inventory_num": 3809, "year": 1754, "period": ["1754-01-01", "1754-12-31"]},
    {"inventory_num": 3810, "year": 1755, "period": ["1755-01-01", "1755-12-31"]},
    {"inventory_num": 3811, "year": 1756, "period": ["1756-01-01", "1756-12-31"]},
    {"inventory_num": 3812, "year": 1757, "period": ["1757-01-01", "1757-12-31"]},
    {"inventory_num": 3813, "year": 1758, "period": ["1758-01-01", "1758-12-31"]},
    {"inventory_num": 3814, "year": 1759, "period": ["1759-01-01", "1759-12-31"]},
    {"inventory_num": 3815, "year": 1760, "period": ["1760-01-01", "1760-12-31"]},
    {"inventory_num": 3816, "year": 1761, "period": ["1761-01-01", "1761-12-31"]},
    {"inventory_num": 3817, "year": 1762, "period": ["1762-01-01", "1762-12-31"]},
    {"inventory_num": 3818, "year": 1763, "period": ["1763-01-01", "1763-12-31"]},
    {"inventory_num": 3819, "year": 1764, "period": ["1764-01-01", "1764-12-31"]},
    {"inventory_num": 3820, "year": 1765, "period": ["1765-01-01", "1765-12-31"]},
    {"inventory_num": 3821, "year": 1766, "period": ["1766-01-01", "1766-12-31"]},
    {"inventory_num": 3822, "year": 1767, "period": ["1767-01-01", "1767-12-31"]},
    {"inventory_num": 3823, "year": 1768, "period": ["1768-01-01", "1768-12-31"]},
    {"inventory_num": 3824, "year": 1769, "period": ["1769-01-01", "1769-12-31"]},
    {"inventory_num": 3825, "year": 1770, "period": ["1770-01-01", "1770-12-31"]},
    {"inventory_num": 3826, "year": 1771, "period": ["1771-01-01", "1771-12-31"]},
    {"inventory_num": 3827, "year": 1772, "period": ["1772-01-01", "1772-12-31"]},
    {"inventory_num": 3828, "year": 1773, "period": ["1773-01-01", "1773-12-31"]},
    {"inventory_num": 3829, "year": 1774, "period": ["1774-01-01", "1774-12-31"]},
    {"inventory_num": 3830, "year": 1775, "period": ["1775-01-01", "1775-12-31"]},
    {"inventory_num": 3831, "year": 1776, "period": ["1776-01-01", "1776-12-31"]},
    {"inventory_num": 3832, "year": 1777, "period": ["1777-01-01", "1777-12-31"]},
    {"inventory_num": 3833, "year": 1778, "period": ["1778-01-01", "1778-12-31"]},
    {"inventory_num": 3834, "year": 1779, "period": ["1779-01-01", "1779-12-31"]},
    {"inventory_num": 3835, "year": 1780, "period": ["1780-01-01", "1780-12-31"]},
    {"inventory_num": 3836, "year": 1781, "period": ["1781-01-01", "1781-06-30"]},
    {"inventory_num": 3837, "year": 1781, "period": ["1781-07-01", "1781-12-31"]},
    {"inventory_num": 3838, "year": 1782, "period": ["1782-01-01", "1782-06-30"]},
    {"inventory_num": 3839, "year": 1782, "period": ["1782-07-01", "1782-12-31"]},
    {"inventory_num": 3840, "year": 1783, "period": ["1783-01-01", "1783-06-30"]},
    {"inventory_num": 3841, "year": 1783, "period": ["1783-07-01", "1783-12-31"]},
    {"inventory_num": 3842, "year": 1784, "period": ["1784-01-01", "1784-06-30"]},
    {"inventory_num": 3843, "year": 1784, "period": ["1784-07-01", "1784-12-31"]},
    {"inventory_num": 3844, "year": 1785, "period": ["1785-01-01", "1785-06-30"]},
    {"inventory_num": 3845, "year": 1785, "period": ["1785-07-01", "1785-12-31"]},
    {"inventory_num": 3846, "year": 1786, "period": ["1786-01-01", "1786-06-30"]},
    {"inventory_num": 3847, "year": 1786, "period": ["1786-07-01", "1786-12-31"]},
    {"inventory_num": 3848, "year": 1787, "period": ["1787-01-01", "1787-06-30"]},
    {"inventory_num": 3849, "year": 1787, "period": ["1787-07-01", "1787-12-31"]},
    {"inventory_num": 3850, "year": 1788, "period": ["1788-01-01", "1788-06-30"]},
    {"inventory_num": 3851, "year": 1788, "period": ["1788-07-01", "1788-12-31"]},
    {"inventory_num": 3852, "year": 1789, "period": ["1789-01-01", "1789-12-31"]},
    {"inventory_num": 3853, "year": 1790, "period": ["1790-01-01", "1790-12-31"]},
    {"inventory_num": 3854, "year": 1791, "period": ["1791-01-01", "1791-06-30"]},
    {"inventory_num": 3855, "year": 1791, "period": ["1791-07-01", "1791-12-31"]},
    {"inventory_num": 3856, "year": 1792, "period": ["1792-01-01", "1792-06-30"]},
    {"inventory_num": 3857, "year": 1792, "period": ["1792-07-01", "1792-12-31"]},
    {"inventory_num": 3858, "year": 1793, "period": ["1793-01-01", "1793-06-30"]},
    {"inventory_num": 3859, "year": 1793, "period": ["1793-07-01", "1793-12-31"]},
    {"inventory_num": 3860, "year": 1794, "period": ["1794-01-01", "1794-06-30"]},
    {"inventory_num": 3861, "year": 1794, "period": ["1794-07-01", "1794-12-31"]},
    {"inventory_num": 3862, "year": 1795, "period": ["1795-01-01", "1795-06-30"]},
    {"inventory_num": 3863, "year": 1795, "period": ["1795-07-01", "1795-12-31"]},
    {"inventory_num": 3864, "year": 1796, "period": ["1796-01-01", "1796-12-31"]}
]
