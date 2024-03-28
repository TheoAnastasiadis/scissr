import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  Link,
  Chip,
} from "@nextui-org/react";
import Logo from "../branding/logo";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck } from "@fortawesome/free-solid-svg-icons";

function Check() {
  return (
    <FontAwesomeIcon
      icon={faCheck}
      border={true}
      style={{ borderColor: "transparent" }}
    />
  );
}

export function PlatformNavbar() {
  return (
    <Navbar isBordered>
      <NavbarBrand>
        <Logo />
      </NavbarBrand>
      <NavbarContent className="hidden sm:flex gap-4" justify="center">
        <NavbarItem>
          <Chip color="success" variant="shadow" startContent={Check()}>
            Contacts
          </Chip>
        </NavbarItem>
        <NavbarItem isActive>
          <Chip color="success" variant="shadow" startContent={Check()}>
            Grid
          </Chip>
        </NavbarItem>
        <NavbarItem>
          <Chip color="success" variant="shadow" startContent={Check()}>
            Chat
          </Chip>
        </NavbarItem>
      </NavbarContent>
      <NavbarContent justify="end">
        <NavbarItem>hello, user_name</NavbarItem>
        <NavbarItem className="hidden py-3 lg:flex">
          <div className="relative rounded-full w-12 h-12 bg-white bg-[url('https://images.pexels.com/photos/5845278/pexels-photo-5845278.jpeg')] bg-cover">
            <div className="absolute bottom-0 right-0 h-5 w-5 rounded-full bg-sucess-700 border-2 border-black-500"></div>
          </div>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
}
