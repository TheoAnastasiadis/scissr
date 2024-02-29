import { Card, CardFooter, CardHeader, Button } from "@nextui-org/react";

function featuredCard() {
  return (
    <Card isFooterBlurred radius="lg" className="border-none">
      <CardHeader className="absolute z-10 top-1 flex-col !items-start">
        <p className="text-tiny text-white/60 uppercase font-bold">
          What to watch
        </p>
        <h4 className="text-white font-medium text-large">
          Stream the Acme event
        </h4>
      </CardHeader>
      <img
        alt="Woman listing to music"
        className="object-cover saturate-75 brightness-75"
        height={400}
        src="https://images.unsplash.com/photo-1519671845924-1fd18db430b8?q=80&w=1908&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        width={350}
      />
      <CardFooter className="justify-between before:bg-white/10 border-white/20 border-1 overflow-hidden py-1 absolute before:rounded-xl rounded-large bottom-1 w-[calc(100%_-_8px)] shadow-small ml-1 z-10">
        <p className="text-tiny text-white/80">Available soon.</p>
        <Button
          className="text-tiny text-white bg-black/20"
          variant="flat"
          color="default"
          radius="lg"
          size="md"
        >
          Notify me
        </Button>
      </CardFooter>
    </Card>
  );
}

export default function Featured() {
  return (
    <section className="container my-10">
      <div className="flex flex-row justify-center space-x-10">
        {featuredCard()}
        {featuredCard()}
        {featuredCard()}
      </div>
    </section>
  );
}
