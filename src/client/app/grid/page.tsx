import { randomBytes } from "crypto";

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

function User(user: { userName: string; online: boolean }) {
  return (
    <div className="relative w-full aspect-square rounded-2xl rounded-tr-3xl rounded-bl-none overflow-hidden border-none">
      <img
        src={
          "https://xsgames.co/randomusers/assets/avatars/female/" +
          parseInt(Math.random() * 30) +
          ".jpg"
        }
        alt="Profile Picture"
      />
      <div className="absolute -bottom-1 -left-1 bg-black-500 rounded-xl rounded-br-none rounded-tl-none py-0.5 px-4 text-sm">
        {user.userName}
      </div>
      {user.online ? (
        <div className="absolute top-0 right-0 h-6 w-6 rounded-full bg-sucess-700 border-[5px] border-black-500"></div>
      ) : null}
    </div>
  );
}

export default function Grid() {
  return (
    <>
      <div className="w-full pb-4">
        <h1 className="text-4xl font-protest text-center w-full">
          ✂sci<span className="text-primary-700">ss</span>r
        </h1>
      </div>
      <div className="font-archivo">
        <nav className="flex flex-row space-x-1">
          <div className="relative rounded-full w-16 h-16 bg-white bg-[url('https://images.pexels.com/photos/5845278/pexels-photo-5845278.jpeg')] bg-cover">
            <div className="absolute bottom-0 right-0 h-5 w-5 rounded-full bg-sucess-700 border-2 border-black-500"></div>
          </div>
          <section className="px-4 py-2">
            <h3 className="text-3xl">Hi, user_name!</h3>
            <p className="font-sans">
              Current Location:&nbsp;
              <span className="font-semibold underline">Athens, Greece</span>
            </p>
          </section>
        </nav>
        <div className="flex flex-row justify-between pt-5">
          <div className="bg-primary-500 rounded-2xl text-black-900 px-2.5 py-1.5">
            (3) Active Filters&nbsp;
          </div>
          <div className="bg-sucess-500 rounded-2xl text-black-900 px-2.5 py-1.5 font-thin">
            Best Match 🔼
          </div>
        </div>
        <main className="grid grid-cols-3 gap-3 pt-5">
          {generateRandomUsers(20).map((u) => User(u))}
        </main>
      </div>
    </>
  );
}
