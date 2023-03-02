import { IconExternalLink } from "@tabler/icons-react";
import { FC } from "react";
// import cover from "../public/cover.png";

export const Navbar: FC = () => {
  return (
    <div className="flex h-[60px] border-b border-gray-300 py-2 px-8 items-center justify-between">
      <div className="font-bold text-2xl flex items-center">
        {/* <Image
          className="hidden sm:flex"
          src={cover}
          alt="The Network State GPT"
          width={30}
          height={30}
        /> */}
        <div className="ml-2">Paul Graham GPT</div>
      </div>
      <div>
        <a
          className="flex items-center hover:opacity-50"
          href="http://www.paulgraham.com/articles.html"
          target="_blank"
          rel="noreferrer"
        >
          <div className="hidden sm:flex">Official Site</div>

          <IconExternalLink
            className="ml-1"
            size={20}
          />
        </a>
      </div>
    </div>
  );
};
