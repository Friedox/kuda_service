import '../../styles/mobile/style.css';
import LocationSelectSection from "../../components/mobile/LocationSelectSection";

function TripFilter() {
    return (
        <>
            <section className="mobile_section">
                <LocationSelectSection />
            </section>
            <div className='gray_bg'/>
        </>
    );
}

export default TripFilter;
