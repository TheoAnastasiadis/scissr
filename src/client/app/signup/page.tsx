"use client";
import { useState } from "react";

/* eslint-disable @next/next/no-img-element */
function Tab(id: number, next: () => void, prev?: () => void) {
  switch (id) {
    case 0:
      return (
        <>
          <div className="bg-black-500 absolute top-0 left-0 px-9 py-5 rounded-br-2xl">
            <p className="text-center text-3xl tracking-widest font-protest">
              sci<span className="text-primary-500">ss</span>r
            </p>
          </div>
          <img
            src="https://images.pexels.com/photos/5838314/pexels-photo-5838314.jpeg"
            alt="background"
            className="rounded-2xl h-[75vh] object-cover"
          />
          <div className="bg-black-500 absolute bottom-0 right-0 rounded-tl-2xl px-9 py-5">
            <p className="font-protest tracking-wider text-center text-xl font-semibold">
              get{" "}
              <button
                className="text-sucess-500 tracking-widest"
                onClick={next}
              >
                started
              </button>
            </p>
          </div>
        </>
      );

    case 1:
      return (
        <form action="#" method="GET" className="space-y-6">
          <h1 className="font-protest text-3xl ">Basic Information</h1>
          <section className="pt-3">
            <h2 className="font-archivo text-xl">
              Pick your <span className="text-primary-400">username</span>.
            </h2>

            <input
              type="text"
              className="mt-4 w-full rounded-2xl border border-primary-700 bg-transparent p-3"
              placeholder="username"
            />
          </section>
          <section>
            <h2 className="font-archivo text-xl">
              Enter your <span className="text-primary-400">age</span>.
            </h2>

            <input
              type="number"
              className="mt-4 w-full rounded-2xl border border-primary-700 bg-transparent p-3"
              placeholder="35"
            />
          </section>
          <section>
            <h2 className="font-archivo text-xl">
              Select your <span className="text-primary-400">pronouns</span>.
            </h2>

            <select className="mt-4 w-full rounded-2xl border border-primary-700 bg-transparent p-3 text-gray-300">
              <option value="she/her" selected>
                she/her
              </option>
              <option value="they/them" selected>
                they/them
              </option>
            </select>
          </section>

          <button
            className="relative top-14 rounded-2xl w-full bg-sucess-500 border-2 text-black-500 font-archivo py-3 border-black-500 uppercase"
            onClick={(e) => {
              e.preventDefault();
              next();
            }}
          >
            Save
          </button>
        </form>
      );
    default:
      break;
  }
}

export default function SignUp() {
  const [crntTab, setCrntTab] = useState(0);
  return (
    <div>
      <div
        id="steps"
        className="w-full flex justify-between align-baseline space-x-3 mb-5"
      >
        <div
          className={
            "w-1/4 bg-primary-200 rounded-2xl h-[1.5px] " +
            (crntTab == 0 ? "bg-primary-200" : "bg-primary-700")
          }
          onClick={() => setCrntTab(0)}
        ></div>
        <div
          className={
            "w-1/4 bg-primary-200 rounded-2xl h-[1.5px] " +
            (crntTab == 1 ? "bg-primary-200" : "bg-primary-700")
          }
          onClick={() => setCrntTab(1)}
        ></div>
        <div
          className={
            "w-1/4 bg-primary-200 rounded-2xl h-[1.5px] " +
            (crntTab == 2 ? "bg-primary-200" : "bg-primary-700")
          }
          onClick={() => setCrntTab(2)}
        ></div>
        <div
          className={
            "w-1/4 bg-primary-200 rounded-2xl h-[1.5px] " +
            (crntTab == 3 ? "bg-primary-200" : "bg-primary-700")
          }
          onClick={() => setCrntTab(3)}
        ></div>
        <div
          className={
            "w-1/4 bg-primary-200 rounded-2xl h-[1.5px] " +
            (crntTab == 4 ? "bg-primary-200" : "bg-primary-700")
          }
          onClick={() => setCrntTab(4)}
        ></div>
      </div>
      <div id="steps-container" className="w-full relative pt-6">
        {Tab(crntTab, () => {
          setCrntTab(crntTab + 1);
        })}
      </div>
    </div>
  );
}
