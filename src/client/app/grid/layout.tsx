import { PlatformNavbar } from "@/components/navigation/PlatformNavBar";

export default function GridLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <PlatformNavbar />
      {children}
    </>
  );
}
