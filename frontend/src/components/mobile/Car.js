
function Car({car_name, car_color, number, region, classesName}) {
    const classes = `car_block ${classesName}`;
    return (
        <>
            <div className={classes}>
                <div className="car_info">
                    <h2>{car_name}</h2>
                    <span>{car_color}</span>
                </div>
                <div className="car_number">
                    <span>{number}</span>
                    <div className="car_line"/>
                    <span>{region}</span>
                </div>
            </div>
        </>
    );
}

export default Car;