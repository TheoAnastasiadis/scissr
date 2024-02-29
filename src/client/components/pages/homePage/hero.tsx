import { Spotlight } from "@/components/aceternity/spotlight";
import { faUserPlus, faGlobe } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button } from "@nextui-org/react";
import Image from "next/image";

export default function HomePageHero() {
  return (
    <section>
      <div className="h-[40rem] w-full rounded-md flex md:items-center md:justify-center bg-black/[0.96] antialiased bg-grid-white/[0.02] relative overflow-hidden">
        <Spotlight />
        <div className="flex flex-row items-stretch space-x-10 py-32">
          <div className="flex flex-col justify-center p-4 max-w-4xl  mx-auto relative z-10  w-3/4 pt-20 md:pt-0">
            <h1 className="text-4xl md:text-7xl font-bold text-center bg-clip-text text-transparent bg-gradient-to-b from-neutral-50 to-neutral-400 bg-opacity-50">
              Building the dating community of tomorrow
            </h1>
            <p className="mt-4 font-normal text-base text-neutral-300 max-w-lg text-center mx-auto">
              <strong>scissr</strong> is an amazing dating community founded on
              the principles of respect, inclusivity, and safety. Get involved
              and indulge in this new experience of dating!
            </p>
            <div className="w-full flex flex-col justify-center py-10 space-y-5 max-w-sm mx-auto">
              <Button
                color="primary"
                variant="shadow"
                endContent={<FontAwesomeIcon icon={faUserPlus} />}
              >
                Become a member
              </Button>
              <Button endContent={<FontAwesomeIcon icon={faGlobe} />}>
                Open webview
              </Button>
            </div>
          </div>
          <div className="w-1/4 py-24">
            <Image
              src="/mockup.png"
              width={"230"}
              height={"380"}
              alt="app mockup"
              className="w-full object-contain h-full"
            ></Image>
          </div>
        </div>
      </div>
    </section>
  );
}
