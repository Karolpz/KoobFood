import { Link } from 'react-router-dom';

const NavBar = ({ items }) => {
    return (
        <nav className="navbar">
            <ul>
                {items.map((item, index) => (
                    <li key={index}>
                        <Link to={item.link}>{item.name}</Link>
                    </li>
                ))}
            </ul>
        </nav>
    )
}
export default NavBar;