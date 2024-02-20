function chat() {
  return (
    <div className="flex flex-row justify-start space-x-5 py-4 px-2.5 border-b border-gray-800">
      <div className="rounded-full aspect-square h-14 overflow-hidden">
        <img
          src={`https://xsgames.co/randomusers/assets/avatars/female/${parseInt(
            Math.random() * 30
          )}.jpg`}
          alt="abcd"
        />
      </div>
      <div className="pt-2">
        <h3>
          user_{parseInt(Math.random() * 20)}
          {Math.random() > 0.33 ? (
            <span className="inline-block w-3 h-3 bg-sucess-500 rounded-full border-2 border-black-500"></span>
          ) : null}
        </h3>
        <p
          className={
            "text-gray-500 font-sans text-sm " +
            (Math.random() > 0.23 ? "text-gray-600" : "text-gray-400 font-bold")
          }
        >
          <span className={"text-gray-600"}>
            {`${Math.floor(Math.random() * 24)}:${Math.floor(
              Math.random() * 60
            )}`}
          </span>{" "}
          {Math.random() > 0.13 ? "hey what's up!" : "photo recieved"}
        </p>
      </div>
    </div>
  );
}

export default function Contacts() {
  return (
    <div className="font-archivo">
      <header className="flex flex-row justify-between border-b border-gray-700 pb-4">
        <h1 className="font-protest text-3xl w-full">
          sci<span className="text-primary-500">ss</span>r{" "}
          <span className="font-shadows text-2xl">chats</span>
        </h1>
        <p className="aspect-square p-2 w-max rounded-full border border-gray-600">
          🔼
        </p>
      </header>
      <main>{Array(20).fill({}).map(chat)}</main>
    </div>
  );
}
