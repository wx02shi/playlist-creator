import { type Track } from "@/lib/api";

interface SongListProps {
  suggested: Track[];
  pinned: Track[];
}

const SongList = ({ suggested, pinned }: SongListProps) => {
  return (
    <div className="flex flex-col">
      <h2 className="text-xl font-bold text-gray-800 mb-6">
        Your new playlist
      </h2>

      <div className="flex flex-col space-y-6">
        <div className="space-y-4">
          {pinned.map((song) => (
            <SongCard key={song.id} song={song} isPinned={true} />
          ))}
        </div>

        {suggested.length > 0 && (
          <>
            <div className="border-t border-gray-200 pt-6">
              <h3 className="text-sm font-semibold text-gray-600 mb-4">
                Suggested tracks
              </h3>
              <div className="space-y-4">
                {suggested.map((song) => (
                  <SongCard key={song.id} song={song} isPinned={false} />
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

const SongCard = ({ song, isPinned }: { song: Track; isPinned: boolean }) => {
  const handleAdd = () => {
    console.log(song.id);
  };

  return (
    <div className="flex items-center p-3 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200">
      {song.collection?.imageUrl && (
        <img
          src={song.collection.imageUrl}
          alt={`${song.collection.name} cover`}
          className="w-16 h-16 rounded-md object-cover"
        />
      )}
      <div className={`flex-1 ${song.collection?.imageUrl ? "ml-4" : ""}`}>
        <h3 className="font-medium text-gray-900">{song.title}</h3>
        <p className="text-sm text-gray-600">{song.artists.join(", ")}</p>
      </div>
      {!isPinned && (
        <button
          onClick={handleAdd}
          className="w-8 h-8 flex items-center justify-center rounded-full bg-blue-500 hover:bg-blue-600 transition-colors duration-200"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth="1.5"
            stroke="currentColor"
            className="size-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 4.5v15m7.5-7.5h-15"
            />
          </svg>
        </button>
      )}
    </div>
  );
};

export default SongList;
