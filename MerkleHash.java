import java.awt.List;
import java.security.MessageDigest;
import java.util.ArrayList;
//This class provides a few static create operators, equality tests, and 
//computes the hash from a byte array, Object, or two other MerkleHash instances.
public class MerkleHash {

		ArrayList<Object> input;
		
		// Merkle Root
		Object root;

		//Constructor: given a set of items (e.g., POI), construct a hash tree
		public MerkleHash(ArrayList<Object> in) {
			this.input=in;
			merkle_tree(in);
		}
		
        /*constructs the merkle tree*/
		public void merkle_tree(ArrayList<Object> in) {
			List<Object> tempinput = new ArrayList<Object>();

			for (int i = 0; i < in.size(); i++) {
				tempinput.add(in.get(i));
			}

			List<Object> newinput = getNewNode(tempinput);
			while (newinput.size() != 1) {
				newinput = getNewNode(newinput);
			}

			this.root = newinput.get(0);
		}
        /*builds the new node based on the two children nodes*/
		private List<Object> getNewNode(List<Object> tempinput) {

			List<Object> newinput = new ArrayList<Object>();
			int index = 0;
			while (index < tempinput.size()) {
				// left
				Object left = tempinput.get(index);
				index++;

				// right
				Object right = "";
				if (index != tempinput.size()) {
					right = tempinput.get(index);
				}

				// combine the left and right child and apply sha2 hex to the results
				//currently giving me an error b/c add(obj) is undefined for Object
				Object sha2HexValue = getSHA2HexValue(left.add(right));
				newinput.add(sha2HexValue);
				index++;

			}

			return newinput;
		}

		/**
		 * Return hexed object; not really sure how to apply it to generic object;
		 * but this one deals with String inputs.
		 * @param str
		 * @return
		 */
		public Object getSHA2HexValue(Object str) {
			byte[] cipher_byte;
			try {
				MessageDigest md = MessageDigest.getInstance("SHA-256");
				md.update(((String) str).getBytes());
				cipher_byte = md.digest();
				StringBuilder sb = new StringBuilder(2 * cipher_byte.length);
				for (byte b : cipher_byte) {
					sb.append(String.format("%02x", b & 0xff));
				}
				return (Object)sb;
			} catch (Exception e) {
				e.printStackTrace();
			}

			return "";
		}

		/**
		 * Get Root
		 * 
		 * @return
		 */
		public Object getRoot() {
			return this.root;
		}
		
	    /*FindAuthentication4Item: takes one item as input and returns the set of internal nodes that are needed to compute the root of the Merkle hash tree. 
	     * Every item or internal node needs to contain the information about its position in the tree to allow computing the root when needed. 
	     */
		private  ArrayList<Object> FindAuthentication4Item(Object o){
			List<Object> internalnodes = new ArrayList<Object>();
			int index = this.input.indexOf(o);
			/*compute the locations of the internal nodes; locate them in the list and append them to the results*/
			return internalnodes;
		}
		
		/*VerifyItem: takes one item and the set of internal nodes as input and returns true if they can compute the correct Merkle Hash tree root.*/
		public boolean verifyItem(ArrayList<Object> innodes, Object o) {
			/*placeholder*/
			return false;
		}
		
		/*FindAuthentication4Set: takes a subset of items as input and returns the set of internal nodes that are needed to compute the root of the Merkle hash tree for every input item.
		 *  This is a generalization of the FindAuthentication4Item method.
		 */
		private  ArrayList<ArrayList<Object>> FindAuthentication4Set(ArrayList<Object> o){
			List<ArrayList<Object>> internalnodes = new ArrayList<ArrayList<Object>>();
			int index = this.input.indexOf(o);
			/*compute the locations of the internal nodes; locate them in the list and append them to the results*/
			return internalnodes;
		}
		
		/*VerifySet: takes a subset of items and the set of internal nodes as input and returns true if we can compute the correct Merkle Hash tree root for EVERY input item.
		 *  This is a generalization of the VerifyItem method. 
		 */
		public boolean verifySet(ArrayList<ArrayList<Object>> innodes, Object o) {
			/*placeholder*/
			return false;
		}
		


 
  }

