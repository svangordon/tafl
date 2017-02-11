Program Requirements:

-- Represent a h'tafl board, on which we can make moves
-- A challenging computer opponent
-- Multiplayer

-- God, I don't want to have to configure webpack

-- Oh my god, do all of the fucking AI server side. Of course!

-- Okay, so the client can be dumb. It should do as little calculation as possible.
  -- Server sends the state of the board, which can include what all of the legal
  moves are. Client doesn't need to figure out what the legal moves are, or what's
  a legal move, etc.
  -- Similarly, the client doesn't need to (say) check to see the if game clock
  has run out, it just timestamps moves. There's probably a way to ensure the
  authenticity of timestamps too (is there?)

-- That means that I can start on the code for the backend without having to
create a frontend! Yay!
  -- Come to think of it, I can write the backend in any language I want! Well
  maybe not any language, but I can write it in Python. Let's do that.

  Classes:
    Board:
      attr: size
            contents(?): one dimensional array w/ piece objects
      methods:
        move piece
        print

    Piece:
      Individual pieces on the board
      attr:
        type
        owner
        position(?)
      methods:
        Doesn't need any

      Square:
        attr: Bool throne
              contents
        methods:
          add / remove piece
          get_moves: all legal moves for a piece on the square

further thoughts: we don't need all these classes. We just need a function that,
when given a board and a position, returns all possible moves for that position.
Also, I'm moving from a one dimensional array to a two dimensional array, because
it means that we don't have to keep passing the size around? Nope, actually, size
is going to be the square root of the length of the array. Yaaay
