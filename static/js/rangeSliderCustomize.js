$("#destination-price-slider, #attraction-price-slider, #accommodation-price-slider").ionRangeSlider({
    skin: "square",

    // type: "double" can make 2 alterable points
    type: "double",
    min: 0,
    max: 1000,

    // need get the real price from the database
    from: 100,
    to: 800,

    prefix: "$",
    hide_min_max: true,
    hide_from_to: false,

    // Fixed position of the starting point and the ending point
    from_fixed: true,
    to_fixed: true,
});