export default function GridLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="md:max-w-[500px] bg-black-500 mx-auto p-4">{children}</div>
  );
}
