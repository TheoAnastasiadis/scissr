import { randomBytes, randomInt } from "crypto";
import {
  Divider,
  Button,
  Card,
  CardBody,
  CardFooter,
  Avatar,
  Navbar,
  NavbarContent,
  NavbarItem,
} from "@nextui-org/react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCaretUp } from "@fortawesome/free-solid-svg-icons/faCaretUp";
import {
  faCircleInfo,
  faLocation,
  faPaperPlane,
  faUserFriends,
} from "@fortawesome/free-solid-svg-icons";
import { faUser } from "@fortawesome/free-regular-svg-icons";
import { faEllipsisVertical } from "@fortawesome/free-solid-svg-icons/faEllipsisVertical";

const generateRandomUsers = (length: number) =>
  Array(length)
    .fill({})
    .map(() => ({
      userName: `user_${Math.floor(Math.random() * 10)}`,
    }))
    .map((u) => ({
      ...u,
      online: Math.random() > 0.5,
    }));

function OnlineBadge(isOnline: boolean) {
  if (isOnline)
    return (
      <div className="ml-2 h-2 w-2 rounded-full bg-green-400 inline-block"></div>
    );
  else return null;
}

function User(user: { userName: string; online: boolean }) {
  return (
    <Card shadow="sm" isPressable isFooterBlurred>
      <CardBody className="overflow-visible p-0">
        <img
          width="100%"
          alt={user.userName}
          className="w-full object-cover h-[140px]"
          src={`https://xsgames.co/randomusers/assets/avatars/female/${randomInt(
            0,
            78
          )}.jpg`}
          className="shaddow-sm rounded-lg"
        />
      </CardBody>
      <CardFooter className="text-small before:bg-white/10 border-white/20 border-1 overflow-hidden py-1 absolute before:rounded-xl rounded-large bottom-1 w-[calc(100%_-_8px)] shadow-small ml-1 z-10">
        <b>{user.userName}</b>
        {OnlineBadge(user.online)}
      </CardFooter>
    </Card>
  );
}

function Radar() {
  return (
    <>
      <div>
        <div className="flex flex-row justify-between pt-5">
          <Button startContent={<span>(3)</span>}>Selected Filters</Button>
          <div className="bg-sucess-500 rounded-2xl text-black-900 px-2.5 py-1.5 font-thin">
            Best Match{" "}
            <FontAwesomeIcon icon={faCaretUp} className="translate-y-0.5" />
          </div>
        </div>
        <main className="grid grid-cols-3 gap-3 pt-5">
          {generateRandomUsers(20).map((u) => User(u))}
        </main>
      </div>
    </>
  );
}

function Contact(user: { userName: string; online: boolean }) {
  return (
    <>
      <div className="flex flex-row py-2.5 hover:bg-slate-900 bg-opacity-55 cursor-pointer transition-colors duration-1000">
        <Avatar
          size="lg"
          src={`https://xsgames.co/randomusers/assets/avatars/female/${randomInt(
            0,
            78
          )}.jpg`}
        />
        <div className="px-2.5 w-[80%]">
          <h3 className="font-semibold">
            {user.userName} {OnlineBadge(user.online)}
          </h3>
          <p className="text-slate-500 italic">wbu?</p>
        </div>
        <div className="justify-self-end">
          <FontAwesomeIcon
            icon={faPaperPlane}
            className="text-slate-500 translate-y-[75%]"
          ></FontAwesomeIcon>
        </div>
      </div>
      <Divider orientation="horizontal"></Divider>
    </>
  );
}

function Contacts() {
  return <>{generateRandomUsers(20).map((u) => Contact(u))}</>;
}

function Chat() {
  return (
    <>
      <Navbar isBordered position="static" className="py-2">
        <NavbarContent justify="start">
          <NavbarItem>
            <Avatar
              size="lg"
              src={`https://xsgames.co/randomusers/assets/avatars/female/${randomInt(
                0,
                78
              )}.jpg`}
            />
          </NavbarItem>
          <NavbarItem>your_crush {OnlineBadge(true)}</NavbarItem>
        </NavbarContent>
        <NavbarContent justify="end">
          <NavbarItem>
            <FontAwesomeIcon
              icon={faEllipsisVertical}
              size="lg"
              className="my-auto"
            />
          </NavbarItem>
        </NavbarContent>
      </Navbar>
      <div className="sticky top-10 min-h-[50vh] bg-green-400"></div>
    </>
  );
}

export default function Grid() {
  return (
    <>
      <section className="flex flex-row">
        <div className="w-3/12 p-5 border-r border-gray-800 h-screen overflow-y-scroll">
          <h2 className="font-inter text-2xl mb-2">Contacts</h2>
          {Contacts()}
        </div>
        <div className="p-5 h-screen overflow-y-scroll w-6/12">
          <h2 className="font-inter text-2xl">
            Grid View &nbsp;
            <span className="text-slate-400 text-sm">
              <FontAwesomeIcon icon={faLocation} className="pr-1" />
              Location last updated 3min ago
            </span>
          </h2>
          {Radar()}
        </div>
        <div className="w-3/12 border-l border-gray-800 h-screen">{Chat()}</div>
      </section>
      <footer className="py-10 border-t border-slate-800">1234</footer>
    </>
  );
}
