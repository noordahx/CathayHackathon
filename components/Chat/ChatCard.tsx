import Link from "next/link";
import Image from "next/image";
import { Chat } from "@/types/chat";

const chatData: Chat[] = [
  {
    avatar: "/images/user/Judge_Cathay - Lawrence Fong_Photo.jpg",
    name: "Mr. Lawrence Fong",
    text: "Updated the data.",
    time: 12,
    textCount: 3,
    dot: 3,
  },
  {
    avatar: "/images/user/Judge_Cathay - Annie Ling_Photo_HD.jpg",
    name: "Ms. Annie Ling",
    text: "Okay!",
    time: 12,
    textCount: 0,
    dot: 1,
  },
  {
    avatar: "/images/user/Judge_Cathay - Ingrid Lee_Photo.jpg",
    name: "Ms. Ingrid Lee",
    text: "Done.",
    time: 32,
    textCount: 0,
    dot: 3,
  },
  {
    avatar: "/images/user/Judge_Google Cloud - Michael Yung.png",
    name: "Mr. Michael Yung",
    text: "Great",
    time: 32,
    textCount: 2,
    dot: 6,
  },
  {
    avatar: "/images/user/Judge_iOS Club - Ray Cheung.jpeg",
    name: "Prof. Ray Cheung",
    text: "How are you?",
    time: 32,
    textCount: 0,
    dot: 3,
  },
  {
    avatar: "/images/user/Microsoft - Victor Chong.jpg",
    name: "Mr. Victor Chong",
    text: "Sure.",
    time: 32,
    textCount: 3,
    dot: 6,
  },
];

const ChatCard = () => {
  return (
    <div className="col-span-12 rounded-sm border border-stroke bg-white py-6 shadow-default dark:border-strokedark dark:bg-boxdark xl:col-span-4">
      <h4 className="mb-6 px-7.5 text-xl font-semibold text-black dark:text-white">
        Chats
      </h4>

      <div>
        {chatData.map((chat, key) => (
          <Link
            href="/"
            className="flex items-center gap-5 py-3 px-7.5 hover:bg-gray-3 dark:hover:bg-meta-4"
            key={key}
          >
            <div className="relative h-14 w-14 rounded-full">
              <Image src={chat.avatar} alt="User" width={57} height={56} />
              <span
                className={`absolute right-0 bottom-0 h-3.5 w-3.5 rounded-full border-2 border-white ${
                  chat.dot === 6 ? "bg-meta-6" : `bg-meta-${chat.dot}`
                } `}
              ></span>
            </div>

            <div className="flex flex-1 items-center justify-between">
              <div>
                <h5 className="font-medium text-black dark:text-white">
                  {chat.name}
                </h5>
                <p>
                  <span className="text-sm text-black dark:text-white">
                    {chat.text}
                  </span>
                  <span className="text-xs"> . {chat.time} min</span>
                </p>
              </div>
              {chat.textCount !== 0 && (
                <div className="flex h-6 w-6 items-center justify-center rounded-full bg-primary">
                  <span className="text-sm font-medium text-white">
                    {" "}
                    {chat.textCount}
                  </span>
                </div>
              )}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default ChatCard;
